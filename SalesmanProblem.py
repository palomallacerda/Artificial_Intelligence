# Implementação do caixeiro viajante usando hillclimbing 
# Codigo incompleto ainda

import random

def radomAnswer(tsp):
    cities = list(range(len(tsp)))
    solution = []
    for i in range(len(tsp)):
        randomCity = cities[random.randint(0, len(cities)-1)]
        solution.append(randomCity)
        cities.remove(randomCity)

    return solution


def routeLength(tsp, solution):
    routeLen = 0
    for i in range(len(solution)):
        routeLen += tsp[solution[i-1]][solution[i]]
    return routeLen


def getNeighboors(solution):
    neighboors = []
    for i in range (len(solution)):
        for j in range(i+1, len(solution)):
            neighboor = solution.copy()
            neighboor[i] = solution[j]
            neighboor[j] = solution[i]
            neighboors.append(neighboor)
    return neighboors

def getBestNeighbour(tsp, neighbours):
    bestRouteLen = routeLength(tsp, neighbours[0])
    bestNeighbour = neighbours[0]
    for neighbour in neighbours:
        currentRouteLen = routeLength(tsp, neighbour)
        if(currentRouteLen < bestRouteLen):
            bestRouteLen = currentRouteLen
            bestNeighbour = neighbour
    return bestNeighbour, bestRouteLen

def hillclimbing(tsp):
    currentSolution = radomAnswer(tsp)
    currentRouteLen = routeLength(tsp, currentSolution)
    neighboors= getNeighboors(currentSolution)
    bestneighbour, bestNeithboutRoute = getBestNeighbour(tsp, neighboors)

    while bestNeithboutRoute < currentRouteLen:
        currentSolution = bestneighbour
        currentRouteLen = bestNeithboutRoute
        neighboors = getNeighboors(currentSolution)
        bestneighbour, bestNeithboutRoute = getBestNeighbour(tsp, neighboors)

    return currentSolution, currentRouteLen
# Criando uma matriz das cidaddes
def main():
    tsp = [ [0, 400, 500, 300],
            [400, 0, 300, 500],
            [500, 300, 0, 400],
            [300, 500, 400, 0],
            ]
    print("(Cities | length)")
    print(hillclimbing(tsp))

if __name__=="__main__":
    main()