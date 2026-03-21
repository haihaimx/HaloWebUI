import importlib
from typing import Iterable


class OptionalDependencyError(RuntimeError):
    pass


def format_optional_dependency_error(
    feature: str,
    packages: Iterable[str],
    install_profiles: Iterable[str] | None = None,
    details: str | None = None,
) -> str:
    package_list = ", ".join(packages)
    message = f"{feature} requires optional dependencies: {package_list}."
    if install_profiles:
        profiles = list(install_profiles)
        requirements_examples = ", ".join(
            f"`backend/requirements/{profile}.txt`" for profile in profiles
        )
        install_profile_hint = "`INSTALL_PROFILE={}`".format(
            profiles[0] if len(profiles) == 1 else "<" + "|".join(profiles) + ">"
        )
        message += (
            " Install the matching dependency profile"
            f" (e.g. {requirements_examples} or {install_profile_hint})."
        )
    if details:
        message += f" {details}"
    return message


def require_module(
    module_name: str,
    *,
    feature: str,
    packages: Iterable[str] | None = None,
    install_profiles: Iterable[str] | None = None,
):
    try:
        return importlib.import_module(module_name)
    except ImportError as exc:
        raise OptionalDependencyError(
            format_optional_dependency_error(
                feature=feature,
                packages=packages or [module_name],
                install_profiles=install_profiles,
                details=f"Missing module: `{module_name}`.",
            )
        ) from exc
