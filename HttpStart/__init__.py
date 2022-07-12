import logging
import azure.functions as func
import azure.durable_functions as df

async def main(req: func.HttpRequest, starter: str) -> func.HttpResponse:
    client = df.DurableOrchestrationClient(starter)
    instance_id = req.params.get('instanceId') #Get parameters does not require the instanceid before execution.
    function_name = req.route_params['functionName']

    if instance_id == None:
        instance_id = await client.start_new(function_name)
        logging.info(f"--==[ First ]==--\nOrchestration with ID = '{instance_id}'.")
        return client.create_check_status_response(req, instance_id)

    existing_instance = await client.get_status(instance_id)
    if existing_instance.runtime_status in [df.OrchestrationRuntimeStatus.Completed, df.OrchestrationRuntimeStatus.Failed, df.OrchestrationRuntimeStatus.Terminated, None]:
        instance_id = await client.start_new(function_name, instance_id)
        logging.info(f"--==[ Starting ]==--\nOrchestration with ID = '{instance_id}'.")
        return client.create_check_status_response(req, instance_id)
    else:
        logging.info(f"--==[ Existing ]==--\nOrchestration with ID = '{instance_id}'.")
        return client.create_check_status_response(req, instance_id)