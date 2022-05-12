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
    tsp = [ [0, 30, 84, 56, -1, -1, -1, 75, -1, 80],
            [30, 0, 65, -1, -1, -1, 70,-1, -1, 40],
            [84, 65, 0, 74, 52, 55, -1, 60, 143, 48],
            [56, -1, 74, 0, 135, -1, -1, 20, -1, -1],
            [-1, -1, 52, 135, 0, 70, -1, 122, 98, 80],
            [70, -1, 55, -1, 70, 0, 63, -1, 82, 35],
            [-1, 70, -1, -1, -1, 63, 0, -1, 120, 57],
            [75, -1, 135, 20, 122, -1, -1, 0, -1, -1],
            [-1, -1, 143, -1, 98, 82, 120, -1, 0, -1],
            [80, 40, 48, -1, 80, 35, 57, -1, -1, 0],
            ]
    print("(Cities | length)")
    print(hillclimbing(tsp))

if __name__=="__main__":
    main()