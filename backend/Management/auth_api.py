from flask import jsonify, request
from flask_restful import Api, Resource, reqparse
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from model import db, User


# Register

class Register(Resource):
    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('username', type=str, required=True)
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        parser.add_argument('role', type=str, default= 'user', required=True)

        parser.add_argument('location', type=str, required=True)
        parser.add_argument('pincode', type=str, required=True)
        parser.add_argument('service_type', type=str)
        parser.add_argument('experience', type=float)

        args = parser.parse_args()

        if User.query.filter_by(username=args['username']).first() or User.query.filter_by(email=args['email']).first():
            return {'message': 'Username or email already exists'}, 400

        if args['role'] == 'user':
            hashed_password = generate_password_hash(args['password'])
            user = User(username=args['username'], email=args['email'], password=hashed_password,
                    role= 'user', location= args['location'], pincode= args['pincode'], approved = True)

        elif args['role'] == 'professional':
            hashed_password = generate_password_hash(args['password'])
            user = User(username=args['username'], email=args['email'], password=hashed_password, 
                    role= 'professional', location= args['location'], pincode= args['pincode'], 
                    service_type= args['service_type'], experience= args['experience'], approved= False )


        db.session.add(user)
        db.session.commit()

        return {'message': f"{args['role'].capitalize()} created successfully"}, 200


# Login
 
class Login(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        args = parser.parse_args()

        user = User.query.filter_by(username=args['username']).first()

        if user and check_password_hash(user.password, args['password']):
            access_token = create_access_token(identity=user.role)
            user_info = {
                "id" : user.id,
                "username" : user.username,
                "role" : user.role 
            }
            if user.approved == False:
                return {'message': 'You cannot login until you got approval from admin'}, 400

            return {'access_token': access_token, 'user': user_info}, 200
        else:
            return {'message': 'Invalid credentials'}, 401



# Logout

class Logout(Resource):
    @jwt_required()
    def post(self):
        user_identity = get_jwt_identity()
        return {'message': f'{user_identity['username']} has logged out successfully'}, 200






