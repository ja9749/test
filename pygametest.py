#Region Imports
import pygame
import player
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from random import randint
#End Region

#Region Global Constants
TITLE = 'Maze'

DISPLAY_WIDTH = 1800
DISPLAY_HEIGHT = 1000

BLOCK_SIZE = 10

MAZE_WIDTH = 59
MAZE_HEIGHT = 32

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
#End Region


#Region Methods
def get_neighbours(node, width, height, maze_visited, visit_flag):
	neighbours = []
	i = node[0]
	j = node[1]
	if i - 1 >= 0:
		if not visit_flag or not maze_visited[i - 1][j]:
			neighbours.append([i - 1, j, 2, 8])
	if j - 1 >= 0:
		if not visit_flag or not maze_visited[i][ j - 1]:
			neighbours.append([i, j - 1, 4, 1])
	if i + 1 < height:
		if not visit_flag or not maze_visited[i + 1][j]:
			neighbours.append([i + 1, j, 8, 2])
	if j + 1 < width:
		if not visit_flag or not maze_visited[i][j + 1]:
			neighbours.append([i, j + 1, 1, 4])
	return neighbours

def generate_maze(width, height):

	maze = [[0 for j in range(width)] for i in range(height)]
	maze_visited = [[False for j in range(width)] for i in range(height)]
	unvisited = width * height
	node = [0,0,0,0]
	nodestack = [node]
	maze_visited[node[0]][node[1]] = True
	unvisited -= 1
	end = False
	while unvisited > 0:	
		neighbours = get_neighbours(node, width, height, maze_visited, True)
		if len(neighbours) > 0:
			end = False
			ran = randint(0, len(neighbours) - 1)
			maze[node[0]][node[1]] = maze[node[0]][node[1]] | neighbours[ran][2]
			maze[neighbours[ran][0]][neighbours[ran][1]] = maze[neighbours[ran][0]][neighbours[ran][1]] | neighbours[ran][3]
			nodestack.append(neighbours[ran])
			node = neighbours[ran]
			maze_visited[node[0]][node[1]] = True
			unvisited -= 1
		else:
			if not end:
				end = True
				neighbours = get_neighbours(node, width, height, maze_visited, False)
				ran = randint(0, len(neighbours) - 1)
				ran2 = randint(0, 2)
				if ran2 > 1:
					maze[node[0]][node[1]] = maze[node[0]][node[1]] | neighbours[ran][2]
					maze[neighbours[ran][0]][neighbours[ran][1]] = maze[neighbours[ran][0]][neighbours[ran][1]] | neighbours[ran][3]

				neighbours.remove(neighbours[ran])

			node = nodestack.pop()

	return maze

def draw_maze(gameDisplay, maze, pl, goal_position):
	gameDisplay.fill(WHITE)
	pygame.draw.rect(gameDisplay, BLACK, [BLOCK_SIZE, BLOCK_SIZE, MAZE_WIDTH * 3 * BLOCK_SIZE, MAZE_HEIGHT * 3 * BLOCK_SIZE])
	for i in range(0, MAZE_HEIGHT):
		for j in range(0, MAZE_WIDTH):
			if i == pl.x and j == pl.y:
				pygame.draw.rect(gameDisplay, BLUE, [2 * BLOCK_SIZE +  pl.y * 3 * BLOCK_SIZE, 2 * BLOCK_SIZE + pl.x * 3 * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE])
			elif i == goal_position[0] and j == goal_position[1]:
				pygame.draw.rect(gameDisplay, RED, [2 * BLOCK_SIZE +  goal_position[1] * 3 * BLOCK_SIZE, 2 * BLOCK_SIZE + goal_position[0] * 3 * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE])
			else:
				pygame.draw.rect(gameDisplay, WHITE, [2 * BLOCK_SIZE +  j * 3 * BLOCK_SIZE, 2 * BLOCK_SIZE + i * 3 * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE])
			if maze[i][j] & 1:
				pygame.draw.rect(gameDisplay, WHITE, [3 * BLOCK_SIZE +  j * 3 * BLOCK_SIZE, 2 * BLOCK_SIZE + i * 3 * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE])
			if maze[i][j] & 2:
				pygame.draw.rect(gameDisplay, WHITE, [2 * BLOCK_SIZE +  j * 3 * BLOCK_SIZE, BLOCK_SIZE + i * 3 * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE])
			if maze[i][j] & 4:
				pygame.draw.rect(gameDisplay, WHITE, [BLOCK_SIZE +  j * 3 * BLOCK_SIZE, 2 * BLOCK_SIZE + i * 3 * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE])
			if maze[i][j] & 8:
				 pygame.draw.rect(gameDisplay, WHITE, [2 * BLOCK_SIZE +  j * 3 * BLOCK_SIZE, 3 * BLOCK_SIZE + i * 3 * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE])

def redraw_pl(gameDisplay, last_position, pl):
	pygame.draw.rect(gameDisplay, WHITE, [2 * BLOCK_SIZE +  last_position[1] * 3 * BLOCK_SIZE, 2 * BLOCK_SIZE + last_position[0] * 3 * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE])
	pygame.draw.rect(gameDisplay, BLUE, [2 * BLOCK_SIZE +  pl.y * 3 * BLOCK_SIZE, 2 * BLOCK_SIZE + pl.x * 3 * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE])

def initialise():
	pygame.init()
	pygame.display.set_caption(TITLE)
	gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))

	maze = generate_maze(MAZE_WIDTH, MAZE_HEIGHT)
	pl = player.Player(0, 0)
	goal_position = [MAZE_HEIGHT - 1, MAZE_WIDTH - 1]

	return [gameDisplay, maze, pl, goal_position]

def move_pl(direction, pl, maze):
	px = pl.x
	py = pl.y

	if direction == pygame.K_LEFT and maze[px][py] & 4:
			py -= 1
	elif direction == pygame.K_RIGHT and maze[px][py] & 1:
			py += 1
	elif direction == pygame.K_UP and maze[px][py] & 2:
			px -= 1
	elif direction == pygame.K_DOWN and maze[px][py] & 8:
			px += 1

	return [[pl.x, pl.y], player.Player(px, py)]

def main():
	[gameDisplay, maze, pl, goal_position] = initialise()	
	
	last_position = [pl.x, pl.y]
	gameExit = False
	redraw = True

	draw_maze(gameDisplay, maze, pl, goal_position)
	while not gameExit:

		if goal_position[0] == pl.x and goal_position[1] == pl.y:
			print("You Win!")
			gameExit = True

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				gameExit = True
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					gameExit = True
				else:
					[last_position, pl] = move_pl(event.key, pl, maze)
					redraw = True

		if redraw:
			redraw_pl(gameDisplay, last_position, pl)
			pygame.display.update()
			redraw = False

	pygame.quit()

if __name__ == "__main__":
	main()
	quit()
#End Region
