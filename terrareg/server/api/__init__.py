from .module_details import ApiModuleDetails
from .module_list import ApiModuleList
from .module_provider_details import ApiModuleProviderDetails
from .module_provider_downloads_summary import ApiModuleProviderDownloadsSummary
from .module_search import ApiModuleSearch
from .module_version_create_bitbucket_hook import ApiModuleVersionCreateBitBucketHook
from .module_version_create_github_hook import ApiModuleVersionCreateGitHubHook
from .module_version_create import ApiModuleVersionCreate
from .module_version_import import ApiModuleVersionImport
from .module_version_details import ApiModuleVersionDetails
from .module_version_download import ApiModuleVersionDownload
from .module_version_source_download import ApiModuleVersionSourceDownload
from .module_version_upload import ApiModuleVersionUpload
from .module_versions import ApiModuleVersions
from .namespace_modules import ApiNamespaceModules
from .open_id_callback import ApiOpenIdCallback
from .open_id_initiate import ApiOpenIdInitiate
from .prometheus_metrics import PrometheusMetrics
from .saml_initiate import ApiSamlInitiate
from .saml_metadata import ApiSamlMetadata
from .terraform_well_known import ApiTerraformWellKnown
from .terrareg_admin_authenticate import ApiTerraregAdminAuthenticate
from .terrareg_audit_history import ApiTerraregAuditHistory
from .terrareg_auth_user_groups import ApiTerraregAuthUserGroups
from .terrareg_config import ApiTerraregConfig
from .terrareg_example_details import ApiTerraregExampleDetails
from .terrareg_example_file_list import ApiTerraregExampleFileList
from .terrareg_example_file import ApiTerraregExampleFile
from .terrareg_example_readme_html import ApiTerraregExampleReadmeHtml
from .terrareg_git_providers import ApiTerraregGitProviders
from .terrareg_global_stats_summary import ApiTerraregGlobalStatsSummary
from .terrareg_global_usage_stats import ApiTerraregGlobalUsageStats
from .terrareg_health import ApiTerraregHealth
from .terrareg_initial_setup_data import ApiTerraregInitialSetupData
from .terrareg_is_authenticated import ApiTerraregIsAuthenticated
from .terrareg_module_provider_analytics_token_versions import ApiTerraregModuleProviderAnalyticsTokenVersions
from .terrareg_module_provider_create import ApiTerraregModuleProviderCreate
from .terrareg_module_provider_delete import ApiTerraregModuleProviderDelete
from .terrareg_module_provider_details import ApiTerraregModuleProviderDetails
from .terrareg_module_provider_integrations import ApiTerraregModuleProviderIntegrations
from .terrareg_module_provider_settings import ApiTerraregModuleProviderSettings
from .terrareg_module_provider_versions import ApiTerraregModuleProviderVersions
from .terrareg_module_search_filters import ApiTerraregModuleSearchFilters
from .terrareg_module_version_delete import ApiTerraregModuleVersionDelete
from .terrareg_module_version_details import ApiTerraregModuleVersionDetails
from .terrareg_module_version_examples import ApiTerraregModuleVersionExamples
from .terrareg_module_version_file import ApiTerraregModuleVersionFile
from .terrareg_module_version_publish import ApiTerraregModuleVersionPublish
from .terrareg_module_version_readme_html import ApiTerraregModuleVersionReadmeHtml
from .terrareg_module_version_submodules import ApiTerraregModuleVerisonSubmodules
from .terrareg_module_version_variable_template import ApiTerraregModuleVersionVariableTemplate
from .terrareg_most_downloaded_module_this_week import ApiTerraregMostDownloadedModuleProviderThisWeek
from .terrareg_most_recently_published_module_version import ApiTerraregMostRecentlyPublishedModuleVersion
from .terrareg_namespace_details import ApiTerraregNamespaceDetails
from .terrareg_namespace_modules import ApiTerraregNamespaceModules
from .terrareg_namespaces import ApiTerraregNamespaces
from .terrareg_provider_logos import ApiTerraregProviderLogos
from .terrareg_submodule_details import ApiTerraregSubmoduleDetails
from .terrareg_submodule_readme_html import ApiTerraregSubmoduleReadmeHtml
from .terrareg_user_group_namespace_permissions import ApiTerraregAuthUserGroupNamespacePermissions
from .terrareg_user_group import ApiTerraregAuthUserGroup
from .terrareg_graph_data import ApiTerraregGraphData
from .terrareg_module_provider_redirects import ApiTerraregModuleProviderRedirects
from .terrareg_module_provider_redirect_delete import ApiTerraregModuleProviderRedirectDelete
from .github.github_login_initiate import GithubLoginInitiate
from .github.github_login_callback import GithubLoginCallback
from .github.github_auth_status import GithubAuthStatus
from .github.github_organisations import GithubOrganisations
from .github.github_repositories import GithubRepositories
from .github.github_repository_publish_provider import GithubRepositoryPublishProvider
from .provider import ApiProvider
from .provider_version_download import ApiProviderVersionDownload
from .provider_versions import ApiProviderVersions

from .terraform.v2.gpg_keys import ApiGpgKeys
from .terraform.v2.gpg_key import ApiGpgKey
from .terraform.v2.provider_categories import ApiProviderCategories
from .terraform.v2.provider_download_summary import ApiProviderProviderDownloadSummary
from .terraform.v2.provider import ApiV2Provider
