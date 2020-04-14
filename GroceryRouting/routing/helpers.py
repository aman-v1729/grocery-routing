from __future__ import print_function
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import urllib, json, requests

def getcoords(form, places, warehouse):
	coords = [warehouse]
	for i in range(0, places):
		s1 = "form-"+str(i)+"-Latitude"
		s2 = "form-"+str(i)+"-Longitude"
		coords.append((float(form[s1]), float(form[s2])))
	return coords

def getdemands(form, places):
	demands = [0]
	for i in range(0, places):
		s = "form-"+str(i)+"-Demand"
		demands.append(int(form[s]))
	return demands

def getcapacities(form, riders):
	capacities = []
	for i in range(0, riders):
		s = "form-"+str(i)+"-Capacity"
		capacities.append(int(form[s]))
	return capacities


def getdistmtr(coords):
    # Microsoft Bing API
    url = "https://dev.virtualearth.net/REST/v1/Routes/DistanceMatrix?origins="
    key = "AmKwhh-IbC_WJaRS5TGj-NSADzzuH1HH9WU8DI-i9sbSl8_YXx3aoE2owOY4WNgX"
    n = len(coords)
    origins = ""

    for i in range(0, len(coords)):
        origins += str(coords[i][0])+","+str(coords[i][1])
        if(i!=len(coords)-1):
            origins += ";"

    tempurl = url + origins + "&destinations=" + origins + "&travelMode=driving&key=" + key
    req = requests.get(tempurl).json()
    res = req['resourceSets'][0]['resources'][0]['results']

    distmtr = []
    for i in range(0, n):
        arr = []
        for j in range(0, n):
            if(i!=j):
                arr.append(int(res[i*n+j]['travelDistance']*1000))
            else:
                arr.append(0)
        distmtr.append(arr)
    # print(distmtr)
    return distmtr



def create_data_model(distmtr, demands, capacities):
    """Stores the data for the problem."""
    data = {}
    data['distance_matrix'] = distmtr
    data['demands'] = demands
    data['vehicle_capacities'] = capacities
    data['num_vehicles'] = len(capacities)
    data['depot'] = 0
    return data


def get_solution(data, manager, routing, solution):
    sol = []
    for vehicle_id in range(data['num_vehicles']):
        rout = {}
        arr = []
        index = routing.Start(vehicle_id)
        route_distance = 0
        route_load = 0
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            arr.append(node_index)

            route_load += data['demands'][node_index]

            previous_index = index
            index = solution.Value(routing.NextVar(index))

            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)

        rout['route'] = arr
        rout['load'] = route_load
        rout['distance'] = route_distance/1000
        sol.append(rout)
    return sol


def god(context):
    """Solve the CVRP problem."""
    # Instantiate the data problem.
    data = create_data_model(getdistmtr(context['coords']), context['demands'], context['capacities'])

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)


    # Create and register a transit callback.
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)


    # Add Capacity constraint.
    def demand_callback(from_index):
        """Returns the demand of the node."""
        # Convert from routing variable Index to demands NodeIndex.
        from_node = manager.IndexToNode(from_index)
        return data['demands'][from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(
        demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # null capacity slack
        data['vehicle_capacities'],  # vehicle maximum capacities
        True,  # start cumul to zero
        'Capacity')

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    sol = {}
    if solution:
        sol['check'] = 1
        sol['result'] = get_solution(data, manager, routing, solution)
    else:
        sol['check'] = 0
        sol['result'] = []
    return sol

# coords = []
# coords.append((28.5221, 77.2102))
# coords.append((28.6304,77.2177))
# coords.append((28.6129, 77.2295))
# coords.append((28.5450, 77.1926))
# coords.append((28.5672, 77.2100))
# coords.append((28.5412, 77.1552))
#
# demands = [0,8,6,8,15,15]
#
# capacities = [15,15,15,15]
#
# context = {
#     "demands": demands,
#     "coords": coords,
#     "capacities": capacities
# }
