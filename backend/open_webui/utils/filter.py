import inspect
import logging

from fastapi import HTTPException
from open_webui.utils.plugin import load_function_module_by_id
from open_webui.models.functions import Functions
from open_webui.env import SRC_LOG_LEVELS

log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["MAIN"])


def get_sorted_filter_ids(model: dict):
    """Return sorted filter IDs for the given model.

    J-3-04: Optimized to avoid N+1 queries.
    Previously: get_function_by_id + get_function_valves_by_id per filter (2N queries)
    Now: single batch query for all active filters, build lookup dicts, zero per-id queries.
    """
    # Single query: get all active filter functions (used for both ID validation and priority lookup)
    active_filters = Functions.get_functions_by_type("filter", active_only=True)
    active_filter_map = {f.id: f for f in active_filters}
    enabled_filter_ids = set(active_filter_map.keys())

    # Collect global + model-specific filter IDs
    filter_ids = [f.id for f in active_filters if f.is_global]
    if "info" in model and "meta" in model["info"]:
        filter_ids.extend(model["info"]["meta"].get("filterIds", []))
        filter_ids = list(set(filter_ids))

    # Keep only enabled filters
    filter_ids = [fid for fid in filter_ids if fid in enabled_filter_ids]

    # Build valves lookup in batch (one query per filter, but only for sorting priority)
    # We read valves from the already-loaded function objects where possible
    valves_cache = {}
    for fid in filter_ids:
        valves_cache[fid] = Functions.get_function_valves_by_id(fid)

    def get_priority(function_id):
        valves = valves_cache.get(function_id)
        return valves.get("priority", 0) if valves else 0

    filter_ids.sort(key=get_priority)
    return filter_ids


def get_sorted_filters(model: dict):
    """Return sorted filter function objects for the given model.

    J-3-04: Combined function that returns both sorted IDs and their function objects
    in a single pass, eliminating the N+1 pattern where callers do:
        [Functions.get_function_by_id(fid) for fid in get_sorted_filter_ids(model)]
    """
    active_filters = Functions.get_functions_by_type("filter", active_only=True)
    active_filter_map = {f.id: f for f in active_filters}
    enabled_filter_ids = set(active_filter_map.keys())

    filter_ids = [f.id for f in active_filters if f.is_global]
    if "info" in model and "meta" in model["info"]:
        filter_ids.extend(model["info"]["meta"].get("filterIds", []))
        filter_ids = list(set(filter_ids))

    filter_ids = [fid for fid in filter_ids if fid in enabled_filter_ids]

    valves_cache = {}
    for fid in filter_ids:
        valves_cache[fid] = Functions.get_function_valves_by_id(fid)

    def get_priority(function_id):
        valves = valves_cache.get(function_id)
        return valves.get("priority", 0) if valves else 0

    filter_ids.sort(key=get_priority)
    return [active_filter_map[fid] for fid in filter_ids if fid in active_filter_map]


async def process_filter_functions(
    request, filter_functions, filter_type, form_data, extra_params
):
    skip_files = None

    for function in filter_functions:
        filter = function
        filter_id = function.id
        if not filter:
            continue

        if filter_id in request.app.state.FUNCTIONS:
            function_module = request.app.state.FUNCTIONS[filter_id]
        else:
            function_module, _, _ = load_function_module_by_id(filter_id)
            request.app.state.FUNCTIONS[filter_id] = function_module

        # Prepare handler function
        handler = getattr(function_module, filter_type, None)
        if not handler:
            continue

        # Check if the function has a file_handler variable
        if filter_type == "inlet" and hasattr(function_module, "file_handler"):
            skip_files = function_module.file_handler

        # Apply valves to the function
        if hasattr(function_module, "valves") and hasattr(function_module, "Valves"):
            valves = Functions.get_function_valves_by_id(filter_id)
            function_module.valves = function_module.Valves(
                **(valves if valves else {})
            )

        try:
            # Prepare parameters
            sig = inspect.signature(handler)

            params = {"body": form_data}
            if filter_type == "stream":
                params = {"event": form_data}

            params = params | {
                k: v
                for k, v in {
                    **extra_params,
                    "__id__": filter_id,
                }.items()
                if k in sig.parameters
            }

            # Handle user parameters
            if "__user__" in sig.parameters:
                if hasattr(function_module, "UserValves"):
                    try:
                        params["__user__"]["valves"] = function_module.UserValves(
                            **Functions.get_user_valves_by_id_and_user_id(
                                filter_id, params["__user__"]["id"]
                            )
                        )
                    except Exception as e:
                        log.exception(f"Failed to get user values: {e}")

            # Execute handler
            if inspect.iscoroutinefunction(handler):
                form_data = await handler(**params)
            else:
                form_data = handler(**params)

            # Guard: if a filter handler returns an HTTPException instead of raising,
            # propagate it properly rather than silently corrupting the payload.
            if isinstance(form_data, HTTPException):
                raise form_data

        except Exception as e:
            log.debug(f"Error in {filter_type} handler {filter_id}: {e}")
            raise e

    # Handle file cleanup for inlet
    if skip_files and "files" in form_data.get("metadata", {}):
        del form_data["files"]
        del form_data["metadata"]["files"]

    return form_data, {}
