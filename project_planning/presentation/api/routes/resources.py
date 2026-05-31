from flask import request
from flask_restx import Namespace, Resource, fields

from presentation.api.dependencies import get_container
from presentation.api.serializers import resource_to_dict


ns_resources = Namespace("resources", description="Resource operations")

resource_input = ns_resources.model(
    "ResourceInput",
    {
        "name": fields.String(required=True, example="Alice"),
        "resource_type": fields.String(
            required=True,
            description="human | material",
            example="human",
        ),
        "role": fields.String(example="Developer"),
        "skill_level": fields.Integer(example=8),
        "quantity": fields.Integer(example=100),
    },
)

resource_output = ns_resources.model(
    "Resource",
    {
        "id": fields.Integer(readonly=True),
        "name": fields.String,
        "resource_type": fields.String,
        "role": fields.String,
        "skill_level": fields.Integer,
        "quantity": fields.Integer,
    },
)


@ns_resources.route("/")
class ResourceList(Resource):
    @ns_resources.marshal_list_with(resource_output)
    def get(self):
        """List all resources."""
        svc = get_container().get_resource_service()
        return [resource_to_dict(r) for r in svc.get_all_resources()]

    @ns_resources.expect(resource_input, validate=True)
    @ns_resources.marshal_with(resource_output, code=201)
    def post(self):
        """Create a resource (human or material)."""
        svc = get_container().get_resource_service()
        data = request.json
        resource_type = data.get("resource_type", "").lower()
        if resource_type == "human":
            resource = svc.create_human_resource(
                name=data["name"],
                role=data.get("role", ""),
                skill_level=data.get("skill_level", 1),
            )
        elif resource_type == "material":
            resource = svc.create_material_resource(
                name=data["name"],
                quantity=data.get("quantity", 0),
            )
        else:
            ns_resources.abort(400, "resource_type must be 'human' or 'material'")
        return resource_to_dict(resource), 201


@ns_resources.route("/<int:resource_id>")
class ResourceItem(Resource):
    @ns_resources.marshal_with(resource_output)
    @ns_resources.response(404, "Not found")
    def get(self, resource_id: int):
        """Get a resource by ID."""
        svc = get_container().get_resource_service()
        resource = svc.get_resource(resource_id)
        if not resource:
            ns_resources.abort(404, "Resource not found")
        return resource_to_dict(resource)

    @ns_resources.expect(resource_input)
    @ns_resources.marshal_with(resource_output)
    @ns_resources.response(404, "Not found")
    def put(self, resource_id: int):
        """Update a resource."""
        svc = get_container().get_resource_service()
        data = request.json or {}
        allowed = {"name", "role", "skill_level", "quantity"}
        kwargs = {k: v for k, v in data.items() if k in allowed}
        resource = svc.update_resource(resource_id, **kwargs)
        if not resource:
            ns_resources.abort(404, "Resource not found")
        return resource_to_dict(resource)

    @ns_resources.response(204, "Deleted")
    @ns_resources.response(404, "Not found")
    def delete(self, resource_id: int):
        """Delete a resource."""
        svc = get_container().get_resource_service()
        if not svc.delete_resource(resource_id):
            ns_resources.abort(404, "Resource not found")
        return "", 204
