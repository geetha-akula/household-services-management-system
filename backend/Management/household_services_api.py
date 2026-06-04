from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource, reqparse
from model import db, Service, User, ServiceRequest
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from functools import wraps
from datetime import datetime


# API Blueprint
households_bp = Blueprint('households_bp', __name__)

api = Api(households_bp)


# role required function for RBAC 
def roles_required(required_roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            role = get_jwt_identity()

            if role not in  required_roles:
                return {"message": "You don't have the required role to access this resource"}, 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator



# CRUD operations for Services

class ServiceResource(Resource):
    
    # Read
    from  app import cache
    @cache.cached(timeout=2)
    def get(self):
        services = Service.query.all()

        return jsonify([{
            'id': service.id,
            'name': service.name,
            'description': service.description,
            'price': service.price,
            'time_required': service.time_required
        } for service in services])

    # Create
    @jwt_required()
    @roles_required(['admin'])
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('description', type=str)
        parser.add_argument('price', type=float)
        parser.add_argument('time_required', type=float)
        args = parser.parse_args()

        if Service.query.filter_by(name= args['name']).first():
            return {"message": "Service already exists"}, 400

        new_service = Service(name= args['name'], description= args['description'], price= args['price'], time_required= args['time_required'])
        db.session.add(new_service)
        db.session.commit()

        return {"message": "Service created successfully"}, 200

    # Update
    @jwt_required()
    @roles_required(['admin'])
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True, help= "Service ID is required")
        parser.add_argument('name', type=str)
        parser.add_argument('description', type=str)
        parser.add_argument('price', type=float)
        parser.add_argument('time_required', type=float)

        args = parser.parse_args()

        service = Service.query.get(args['id'])

        if not service:
            return {"message": "service not found"}, 404

        service.name = args['name']
        service.description = args['description']
        service.price = args['price']
        service.time_required = args['time_required']

        db.session.commit()
        return {"message": "Service updated successfully"}, 200


    # Delete
    @jwt_required()
    @roles_required(['admin'])
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True, help= "Service ID is required")
        args = parser.parse_args()

        service = Service.query.get(args['id'])
        if not service:
            return {"message": "Service not found"}, 404

        db.session.delete(service)
        db.session.commit()
        return {"message": "Service deleted successfully"}, 200


# Fetch a particular service

class FetchService(Resource):
    @jwt_required()
    @roles_required(['admin'])
    def get(self, id):
        service = Service.query.filter_by(id= id).first()

        if not service:
            return {"message": "Service not found"}, 404
        
        service_data = {
            "id" : service.id,
            "name" : service.name,
            "description" : service.description,
            "price" : service.price,
            "time_required" : service.time_required
        }

        return service_data, 200


## Service Request API's

# Fetch a specific service request

class FetchServiceRequest(Resource):
    @jwt_required()
    @roles_required(['user'])
    def get(self, id):
        service_request = ServiceRequest.query.filter_by(id= id).first()

        if not service_request:
            return {"message": "Service request not found"}, 404

        request_data = {
            "id" : service_request.id,
            "rating" : service_request.rating,
            "professional_name": User.query.filter_by(id=service_request.professional_id).first().username,
            "service_name": Service.query.filter_by(id=service_request.service_id).first().name,
            "service_description": Service.query.filter_by(id=service_request.service_id).first().description,

        }
        return request_data, 200




# Fetching all service requests

class ServiceRequestResource(Resource):

    @jwt_required()
    @roles_required(['admin'])
    def get(self):
        service_requests = ServiceRequest.query.all()

        data = []
        
        for request in service_requests:
            data.append({
                "id": request.id,
                "requested_date": request.requested_date.strftime("%Y-%m-%d"),
                "completion_date": request.completion_date.strftime("%Y-%m-%d") if request.completion_date else None,
                "rating": request.rating,
                "service_status": request.service_status,
                "customer_name": User.query.filter_by(id=request.customer_id).first().username,
                "professional_name": User.query.filter_by(id=request.professional_id).first().username,
                "service_name": Service.query.filter_by(id=request.service_id).first().name
            })
        return data, 200


#  Requesting a Service API

class CreateServiceRequest(Resource):
    
    # Create a service request
    @jwt_required()
    @roles_required(['user'])
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('service_id', type=int, required=True)
        parser.add_argument('customer_id', type=str, required=True)
        parser.add_argument('professional_id', type=str, required=True)
        args = parser.parse_args()

        existing_request = ServiceRequest.query.filter_by(
                           customer_id = args['customer_id'],
                           professional_id = args['professional_id']
                        ).filter(ServiceRequest.service_status != 'closed').first()
        
        if existing_request:
            return {
                "message": "You already have a pending request with this professional."
            }, 400

        
        new_service_request = ServiceRequest(service_id= args['service_id'],
                            customer_id= args['customer_id'], professional_id= args['professional_id'],
                            requested_date= datetime.now().date())
        db.session.add(new_service_request)
        db.session.commit()

        return {"message": "Service request created successfully"}, 201


# Cancel the service request API

class CancelServiceRequest(Resource):

    @jwt_required()
    @roles_required(['user'])
    def delete(self, id):
        
        service_request = ServiceRequest.query.filter_by(id= id).first()

        db.session.delete(service_request)
        db.session.commit()

        return {"message": "Service request canceled successfully"}, 200


# Access the service request API

class AcceptServiceRequest(Resource):
    @jwt_required()
    @roles_required(['professional'])
    def post(self, id):
        request = ServiceRequest.query.filter_by(id= id).first()
        
        if not request:
            return {"message": "Service request not found"}, 404

        request.service_status = "assigned"
        db.session.commit()
        return {"message": "Service request accepted successfully"}, 200


# Reject the service request API

class RejectServiceRequest(Resource):
    @jwt_required()
    @roles_required(['professional'])
    def delete(self, id):
        request = ServiceRequest.query.filter_by(id= id).first()

        if not request:
            return {"message": "Service request not found"}, 404

        if request.service_status == "requested":
            db.session.delete(request)
            db.session.commit()
            return {"message": "Service request rejected successfully"}, 200


# Close the service request API

class CloseServiceRequest(Resource):
    @jwt_required()
    @roles_required(['user'])
    def put(self, id):
        request = ServiceRequest.query.filter_by(id= id).first()

        if not request:
            return {"message": "Service request not found"}, 404

        if request.service_status == "assigned":
            request.service_status = "closed"
            request.completion_date = datetime.now().date()

            db.session.commit()
            return {"message": "Service request closed successfully"}, 200
            


# Get all users

class AllUsers(Resource):
    @jwt_required()
    def get(self):
        users = User.query.all()
        user_info = [{
                       "id" : user.id,
                       "username" : user.username,
                       "email" : user.email
                    } for user in users]

        return user_info


# fetch all customers 

class CustomerResource(Resource):
    @jwt_required()
    @roles_required(['admin'])
    def get(self):
        try:
            users = User.query.filter_by(role='user').all()
            user_data = [{
                        "id" : user.id,
                        "username" : user.username,
                        "email" : user.email,
                        "location" : user.location,
                        "pincode" : user.pincode
                        } for user in users]

            return user_data, 200
        except Exception as e:
            return {"message": str(e)}, 500



# fetch a specific user
class UserResource(Resource):
     @jwt_required()
     @roles_required(['user','professional'])
     def get(self, id):
        user = User.query.filter_by(id= id).first()
        
        if not user:
            return {"message": "User not found"}, 404

        user_data = {
                       "id" : user.id,
                       "username" : user.username,
                       "email" : user.email,
                       "role" : user.role,
                       "service_type" : user.service_type,
                       "experience" : user.experience,
                       "location" : user.location,
                       "pincode" : user.pincode
                    }

        return user_data, 200


 # User Orders API

class UserOrders(Resource):
    
    # Get user's orders
    @jwt_required()
    @roles_required(['user'])
    def get(self, id):

        service_requests = ServiceRequest.query.filter_by(customer_id=id).all()
        
        orders = [{
                    "id" : request.id,
                    "service_id" : request.service_id,
                    "customer_id" : request.customer_id,
                    "professional_id" : request.professional_id,
                    "service_status" : request.service_status,
                    "rating": request.rating,
                    "requested_date" : request.requested_date.strftime("%Y-%m-%d"),
                    "completion_date" : request.completion_date.strftime("%Y-%m-%d") if request.completion_date else None,
                    "service_name" : Service.query.filter_by(id= request.service_id).first().name,
                    "professional_name" : User.query.filter_by(id= request.professional_id).first().username,
                    "location" : User.query.filter_by(id= request.professional_id).first().location,
        } for request in service_requests]

        return orders, 200


# User feedback for a service

class Feedback(Resource):

    @jwt_required()
    @roles_required(['user'])
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True)
        parser.add_argument('rating', type=int, required=True)
        args = parser.parse_args()

        request = ServiceRequest.query.filter_by(id=args['id']).first()
        
        if not request:
            return {"message": "Service request not found"}, 404

        request.rating = args['rating']
        db.session.commit()
        return {"message": "Feedback submitted successfully"}, 200



# Pending Professionals API

class PendingProfessional(Resource):

    
    # Get pending professionals
    @jwt_required()
    @roles_required(['admin'])
    def get(self):
        pending_professionals = User.query.filter_by(approved= False, role= 'professional').all()

        pending_professionals_data = []

        for professional in pending_professionals:
            professional_data = {
                "id" : professional.id,
                "username" : professional.username,
                "email" : professional.email,
                "service_type" : professional.service_type,
                "experience" : professional.experience,
                "location" : professional.location,
                "pincode" : professional.pincode
            }
            pending_professionals_data.append(professional_data)

        return pending_professionals_data, 200


    # Approve/Reject Professional
    @jwt_required()
    @roles_required(['admin'])
    def post(self):
        data = request.get_json()

        professional_id = data.get('professional_id')
        status = data.get('status')

        if not professional_id or status not in ['approve', 'reject']:
            return {'message': 'Invalid request'}, 400

        user = User.query.get(professional_id)

        if not user:
            return {'message': 'Professional not found'}, 404

        if status == 'approve':
            user.approved = True
        elif status == 'reject':
            db.session.delete(user)
        db.session.commit()

        return {'message': 'Professional status updated successfully'}, 200


#  Fetching all approved professionals

class ApprovedProfessionals(Resource):
    @jwt_required()
    @roles_required(['admin'])
    def get(self):

        try:
            professionals = User.query.filter_by(approved=True, role= 'professional').all()

            if not professionals:
                return {'message': 'No approved professionals found'}, 404

            professionals_data = []

            for professional in professionals:

                professionals_data.append({
                    "id" : professional.id,
                    "username" : professional.username,
                    "email" : professional.email,
                    "location" : professional.location,
                    "pincode" : professional.pincode,
                    "service_type" : professional.service_type,
                    "experience" : professional.experience
                })

            return professionals_data, 200
        
        except Exception as e:
            return {'message': str(e)}, 500




# API for Professionals offering specific service
class ServiceProfessional(Resource):
    @jwt_required()
    @roles_required(['user'])
    def get(self, serviceID):
        try:
            service = Service.query.filter_by(id= serviceID).first()

            if not service:
                return {'message': 'Service not found'}, 404

            professionals = User.query.filter_by(service_type = service.name,
                            role='professional', 
                            approved=True).all()

            if not professionals:
                return {'message': 'No professionals available for this service'}, 404

            professionals_list = [
                {
                    'id': professional.id,
                    'username': professional.username,
                    'email': professional.email,
                    'location': professional.location,
                    'pincode': professional.pincode,
                    'service_type': professional.service_type,
                    'experience': professional.experience,
                    
                }
                for professional in professionals

            ]
            return {"service_name": service.name, "professionals": professionals_list}, 200
        
        except Exception as e:
            return {'message': 'An error occurred', "error": str(e)}, 500


# Getting Service requests of a professional
class ProfessionalServiceRequests(Resource):
    @jwt_required()
    @roles_required(['professional'])
    def get(self, id):
        try:

            professional_requests = ServiceRequest.query.filter_by(professional_id=id).all()


            data = []
            for prequest in professional_requests:
                customer_id = prequest.customer_id
                service_id = prequest.service_id


                customer_requests = ServiceRequest.query.filter_by(customer_id= customer_id, service_id= service_id).all()
                
                assigned_to_other = any(crequest.service_status == "assigned" and
                                        crequest.professional_id!= id
                                        for crequest in customer_requests)

                if assigned_to_other:
                    db.session.delete(prequest)

                else:
                    if prequest.service_status == "requested":
                        customer = User.query.filter_by(id= prequest.customer_id).first()
                        data.append({
                            "id": prequest.id,
                            "customer_name": customer.username,
                            "location": customer.location,
                            "pincode": customer.pincode,
                            "requested_date": prequest.requested_date.strftime('%Y-%m-%d'),
                        })
                        
            db.session.commit()
            return data, 200

        
        except Exception as e:
            return {'message': 'An error occurred while processing the service requests', "error": str(e)}, 500

# Professional Orders API

class ProfessionalOrders(Resource):
    @jwt_required()
    @roles_required(['professional'])
    def get(self, id):
        service_requests = ServiceRequest.query.filter_by(professional_id=id).all()
        orders = []

        for request in service_requests:
            if request.service_status in ['assigned', 'closed']:
                order = {
                    "id" : request.id,
                    "service_status" : request.service_status,
                    "requested_date" : request.requested_date.strftime("%Y-%m-%d"),
                    "completion_date" : request.completion_date.strftime("%Y-%m-%d") if request.completion_date else None,
                    "customer_name" : User.query.filter_by(id= request.customer_id).first().username,
                    "location" : User.query.filter_by(id= request.professional_id).first().location,
                    "rating": request.rating
                }
                orders.append(order)
            
        return orders, 200





# Stats API

class StatPage(Resource):
    @jwt_required()
    @roles_required(['admin'])
    def get(self):
        roles_count = db.session.query(User.role, db.func.count(User.id)).group_by(User.role).all()
        roles_count_dict = {role: count for role, count in roles_count}

        status_count = db.session.query(ServiceRequest.service_status, db.func.count(ServiceRequest.id)).group_by(ServiceRequest.service_status).all()
        status_count_dict = {status: count for status, count in status_count}

        professional_count = (db.session.query(
                            Service.name, db.func.count(User.id))
                            .join(ServiceRequest, Service.id == ServiceRequest.service_id)
                            .join(User, User.id == ServiceRequest.professional_id).group_by(Service.name).all()
                        )

        professional_count_dict = {service: count for service, count in professional_count}

        return jsonify({
            "roles_count": roles_count_dict,
            "status_count": status_count_dict,
            "professional_count": professional_count_dict,
        })




# Routes

api.add_resource(FetchService, '/service/<int:id>')
api.add_resource(ServiceResource, '/service')

api.add_resource(FetchServiceRequest, '/service_request/<int:id>')
api.add_resource(ServiceRequestResource, '/service_requests')
api.add_resource(CreateServiceRequest, '/service_request/create')
api.add_resource(CancelServiceRequest, '/service_request/<int:id>/cancel')
api.add_resource(AcceptServiceRequest, '/service_request/<int:id>/accept')
api.add_resource(RejectServiceRequest, '/service_request/<int:id>/reject')
api.add_resource(CloseServiceRequest, '/service_request/<int:id>/close')


api.add_resource(AllUsers, '/all_users')

api.add_resource(CustomerResource, '/users')
api.add_resource(UserResource, '/user/<int:id>')
api.add_resource(UserOrders, '/user/<int:id>/orders')
api.add_resource(Feedback, '/user/feedback')

api.add_resource(PendingProfessional, '/pending_professionals')
api.add_resource(ApprovedProfessionals, '/professionals')
api.add_resource(ServiceProfessional, '/service/<int:serviceID>/professionals')
api.add_resource(ProfessionalServiceRequests, '/professional/<int:id>/requests')
api.add_resource(ProfessionalOrders, '/professional/<int:id>/orders')


api.add_resource(StatPage, '/stats')