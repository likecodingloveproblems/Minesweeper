import random


class Node:
    def __init__(self, is_bomb, position):
        self.is_bomb = is_bomb
        self.position = position
        self.is_neutralize = False
        self.bomb_neighbours_count = 0
        self.is_clicked = False

    def __str__(self):
        return self.position


    def neutralize(self):
        self.is_neutralize = True

class Game:
    def __init__(self):
        '''generate all nodes'''
        self.width = 10
        self.height = 10
        self.nodes = []
        self.max_bomb = 5
        self.initialize_game()
        self.default_actions = ['q', 'c', 'n', 'u']

    def neighbours(self, node):
        _neighbours = []
        for x in range(node.position[0] - 1, node.position[0] + 2):
            for y in range(node.position[1] - 1, node.position[1] + 2):
                if (x, y) == node.position:
                    continue
                elif x < 0 or x >= self.height:
                    continue
                elif y < 0 or y >= self.width:
                    continue
                _neighbours.append((x, y))
        return _neighbours

    def initialize_game(self):
        '''initialize all nodes and props'''
        self.__create_board()
        self.__assign_bomb()
        self.__update_bomb_neighbours_count()

    def __create_board(self):
        for x in range(self.width):
            row = []
            for y in range(self.height):
                row.append(Node(False, (x, y)))
            self.nodes.append(row)

    def __assign_bomb(self):
        '''assign bomb to nodes'''
        for _ in range(self.max_bomb):
            position = (random.randint(0, self.width - 1), random.randint(0, self.height - 1))
            self.nodes[position[0]][position[1]].is_bomb = True

    def __update_bomb_neighbours_count(self):
        for row in self.nodes:
            for node in row:
                for position in self.neighbours(node):
                    if self.get_node(position).is_bomb:
                        node.bomb_neighbours_count += 1

    def click_node(self, node):
        '''click a node'''
        if node.is_bomb:
            self.fail()
        else:
            self.__click_node(node)

    def __click_node(self, node):
        '''neutralize a node'''
        if node.is_clicked:
            return
        node.is_clicked = True

        if node.bomb_neighbours_count == 0:
            for position in self.neighbours(node):
                neighbour_node = self.get_node(position)
                self.__click_node(neighbour_node)

    def neutralize(self, node):
        '''neutralize a node'''
        node.is_neutralize = True

    def undo_neutralize(self, node):
        '''undo neutralize a node'''
        node.is_neutralize = False

    def draw(self):
        '''draw the game'''
        for row in self.nodes:
            for node in row:
                print('|', end='')
                if node.is_clicked:
                    print(node.bomb_neighbours_count, end='')
                elif node.is_neutralize:
                    print('*', end='')
                else:
                    print('O', end='')

            print('|')

    def check_win(self):
        '''end the game
        we have two scenario for win:
        1. all bomb nodes are neutralized
        2. all normal nodes are clicked'''
        nodes = sum(self.nodes, [])
        bomb_nodes = self.get_bomb_nodes()
        neutralized_node = self.get_neutralized_nodes()
        unneutralized_bomb = list(
            filter(lambda node: not node.is_neutralize, bomb_nodes))
        if len(unneutralized_bomb) == 0:
            return
        if len(neutralized_node) != len(bomb_nodes):
            return
        nodes = sum(self.nodes, [])
        clicked_node = list(filter(lambda node: node.is_clicked, nodes))
        not_clicked_nodes = len(nodes) - len(clicked_node)
        if not_clicked_nodes == self.max_bomb:
            raise Exception('you win')

    def fail(self):
        raise Exception('you fail')

    def save_game(self):
        '''save the game'''

    def get_action(self):
        '''get the action from user'''
        while True:
            action = input('action: ')
            if action not in self.default_actions:
                print('action is invalid')
                continue
            return action

    def get_node(self, position):
        '''get the node by position'''
        return self.nodes[position[0]][position[1]]

    def get_position(self):
        '''get the position from user'''
        while True:
            try:
                position = input('position: ').split(' ')
                position = (int(position[0]), int(position[1]))
            except:
                print('position is invalid')
                continue
            if position[0] >= 0 and position[0] < self.width and position[1] >= 0 and position[1] < self.height:
                return position
            else:
                print('position is invalid')

    def get_bomb_nodes(self):
        '''get all bomb nodes'''
        bomb_nodes = []
        for row in self.nodes:
            for node in row:
                if node.is_bomb:
                    bomb_nodes.append(node)
        return bomb_nodes

    def get_neutralized_nodes(self):
        nodes = sum(self.nodes, [])
        neutralized_nodes = list(filter(lambda node: node.is_neutralize, nodes))
        return neutralized_nodes



    def play(self):
        try:
            while True:
                self.draw()
                action = self.get_action()
                if action == 'q':
                    print('bye')
                    break
                elif action == 'c':
                    position = self.get_position()
                    node = self.get_node(position)
                    self.click_node(node)
                elif action == 'n':
                    position = self.get_position()
                    node = self.get_node(position)
                    self.neutralize(node)
                elif action == 'u':
                    position = self.get_position()
                    node = self.get_node(position)
                    self.undo_neutralize(node)
                self.check_win()
        except Exception as e:
            print(e)

if __name__ == "__main__":
    game = Game()
    game.play()
