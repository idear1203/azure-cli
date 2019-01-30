# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azure.cli.core.decorators import Completer
from ._client_factory import cf_network, cf_graph


# pylint: disable=inconsistent-return-statements
@Completer
def subnet_completion_list(cmd, prefix, namespace, **kwargs):  # pylint: disable=unused-argument
    client = cf_network(cmd.cli_ctx)
    if namespace.resource_group_name and namespace.vnet_name:
        rg = namespace.resource_group_name
        vnet = namespace.vnet_name
        return [r.name for r in client.subnets.list(resource_group_name=rg, virtual_network_name=vnet)]


@Completer
def cluster_admin_account_completion_list(cmd, prefix, namespace, **kwargs):  # pylint: disable=unused-argument
    client = cf_graph(cmd.cli_ctx)
    cluster_admin_account = prefix or ''
    user_names = []
    if cluster_admin_account:
        user_list = client.users.list(filter="startswith(userPrincipalName, '{}')".format(cluster_admin_account)) \
                                .advance_page()
        user_names = [r.mail if r.user_type == "Guest" else r.user_principal_name for r in user_list]
    else:
        user_list = client.users.list().advance_page()
        user_names = [r.mail if r.user_type == "Guest" else r.user_principal_name for r in user_list]
    return user_names
