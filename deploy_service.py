import dtlpy as dl
import logging

logger = logging.getLogger(name='deploy-service')

package_name = "getty-inflation"

class DataLoopFaaS:
    @staticmethod
    def deploy_service(project_name):
        # project = dl.projects.get(project_name=project_name)
        project = dl.projects.get(project_id='e370fbba-7b8a-4f72-abf3-52b079f019e9')

        #################
        # deploy package #
        #################

        slots = [
                 dl.PackageSlot(function_name='inflate_dataset_with_items_from_getty',
                                module_name=package_name,
                                display_scopes=[
                                    dl.SlotDisplayScope(resource=dl.SlotDisplayScopeResource.DATASET_QUERY, filters={}),
                                ],
                                display_icon="icon-dl-download",
                                display_name="Getty Inflate",
                                post_action=dl.SlotPostAction(type=dl.SlotPostActionType.NO_ACTION))
                 ]

        functions = [
            dl.PackageFunction(
                name='inflate_dataset_with_items_from_getty',
                inputs=[
                    dl.FunctionIO(name='dataset', type=dl.PackageInputType.DATASET),
                    dl.FunctionIO(name='number_of_items', type=dl.PackageInputType.INT),
                    dl.FunctionIO(name='phrase', type=dl.PackageInputType.STRING),
                ],
                description='get images from getty based on phrase',
                display_scopes=[
                    dl.SlotDisplayScope(resource=dl.SlotDisplayScopeResource.DATASET_QUERY, filters={},
                                        panel=dl.UiBindingPanel.BROWSER),
                ],
            )
        ]

        modules = [dl.PackageModule(
            name=package_name,
            class_name='ServiceRunner',
            entry_point='main.py',
            functions=functions)]

        package = project.packages.push(package_name=package_name,
                                        modules=modules,
                                        slots=slots,
                                        service_config={
                                            'runtime': dl.KubernetesRuntime(
                                                concurrency=10,
                                                autoscaler=dl.KubernetesRabbitmqAutoscaler(
                                                    min_replicas=0,
                                                    max_replicas=1,
                                                    queue_length=100
                                                )).to_json()},
                                        src_path='.')
        package_version = package.version
        logger.info(f'Package version: {package_version} got deployed !!')

        #################
        # create service #
        #################
        try:
            service = package.services.get(service_name=package.name)
            logger.info("service has been gotten: ", service.name)
        except dl.exceptions.NotFound:
            service = package.services.deploy(service_name=package.name,
                                              module_name=package_name)
            logger.info("service has been deployed: ", service.name)

        logger.info(f"package.version: {package.version}")
        logger.info(f"service.package_revision: {service.package_revision}")
        logger.info(f"service.runtime.concurrency: {service.runtime.concurrency}")
        service.runtime.autoscaler.print()

        if package.version != service.package_revision:
            service.package_revision = package.version
            service.update(force=True)
            logger.info(f"service.package_revision has been updated: {service.package_revision}")

        if slots and len(slots):
            try:
                service.activate_slots(project_id=project.id)
                logger.info("Slots are activated")
            except Exception as e:
                logger.debug(e)
                logger.info("Slots already exists")

if __name__ == '__main__':
    if dl.token_expired():
        dl.login()
    dl.login()
    DataLoopFaaS.deploy_service(project_name='Dataloop demo 2024')