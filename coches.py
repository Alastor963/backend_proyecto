from mesa import Model
from mesa.space import MultiGrid
from mesa import Agent
from collections import defaultdict
from mesa.time import RandomActivation
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid
import os

class RandomActivationByBreed(RandomActivation):

  def __init__(self, model):
    super().__init__(model)
    self.agents_by_breed = defaultdict(dict)

  def add(self, agent):
    self._agents[agent.unique_id] = agent
    agent_class = type(agent)
    self.agents_by_breed[agent_class][agent.unique_id] = agent

  def remove(self, agent):

    del self._agents[agent.unique_id]

    agent_class = type(agent)
    del self.agents_by_breed[agent_class][agent.unique_id]

  def step(self, by_breed = True):

    if by_breed:
      for agent_class in self.agents_by_breed:
        self.step_breed(agent_class)
        self.steps += 1
        self.time += 1
    else:
      super().step()

  def step_breed(self, breed):

    agent_keys = list(self.agents_by_breed[breed].keys())
    self.model.random.shuffle(agent_keys)
    for agent_key in agent_keys:
      self.agents_by_breed[breed][agent_key].step()

  def get_breed_count(self, breed_class):
    return len(self.agents_by_breed[breed_class].values())


class Banquetas(Agent):

  def __init__(self,pos,model, moore = False, orientation = 0):
    super().__init__(pos,model)
    self.pos = pos
    self.orientation = orientation

class Semaforo(Agent):
  def __init__(self,pos, model, moore = False, light = 0, working_time = 0, orientation = 0):
    super().__init__(pos,model)
    self.pos = pos
    self.light = 0
    self.working_time = working_time
    self.orientation = orientation

  def green_light(self):
    self.light = 1

  def red_ligth(self):
    self.light = 0


  def density(self):
    time_este = 0
    time_norte = 0


    if self.orientation == 0:
      total_time = 0
      list = [(0,5), (1,5), (2, 5), (3, 5), (4, 5)]
      trafic_list = self.model.grid.get_cell_list_contents(list)
      for coche in trafic_list:

        coche_time = coche.waiting_time
        total_time += coche_time




      time_este = total_time

      if time_este > time_norte:
        self.green_light()
      if time_este < time_norte:
        self.red_ligth()
      if time_este == time_norte:
        self.red_ligth()


    if self.orientation == 1:


      total_time = 0
      list = [(6, 12), (6,11), (6,10), (6,9), (6, 8), (6,7)]
      trafic_list = self.model.grid.get_cell_list_contents(list)


      for coche in trafic_list:
        self.working_time = coche.waiting_time
        total_time += self.working_time


      time_norte = total_time

      if time_norte > time_este:
        self.green_light()
      if time_norte < time_este:
        self.red_ligth()
      if time_norte == time_este:
        self.red_ligth()






  def step(self):
    self.density()

class Coche(Agent):
  def __init__(self, pos, model, moore = False, length = 0, can_move = True, waiting_time = 0, orientation = 0):
    super().__init__(pos,model)
    self.pos = pos
    self.moore = moore
    self.length = length
    self.can_move = can_move
    self.waiting_time = waiting_time
    self.orientation = orientation

  def move(self):
    if self.can_move == True and self.length < 1:

      if self.orientation == 0:
        next_move = (self.pos[0] + 1, self.pos[1])
        self.model.grid.move_agent(self, next_move)


      if self.orientation == 1:
        next_move = (self.pos[0], self.pos[1] - 1)
        self.model.grid.move_agent(self, next_move)





  def vecinos(self):

    if self.orientation == 0:
      next = (self.pos[0] + 1, self.pos[1])
      next_neig = self.model.grid.get_cell_list_contents([next])

      this_cell = self.model.grid.get_cell_list_contents([next])

      if len(this_cell) < 1:
        self.can_move = True
        self.length = 0



      for agent in next_neig:
        if type(agent) is Coche:
          self.length = 1
          self.waiting_time += 1
          self.can_move = False

        if type(agent) is Semaforo:
          if next_neig[0].light == 0:

            self.can_move = False
            self.waiting_time += 1

          elif next_neig[0].light == 1:
            self.model.grid.move_agent(self, next)





    if self.orientation == 1:

      nexty = (self.pos[0] , self.pos[1] - 1)
      next_neigy = self.model.grid.get_cell_list_contents([nexty])

      this_cell = self.model.grid.get_cell_list_contents([nexty])

      if len(this_cell) < 1:
        self.can_move = True
        self.length = 0

      for agent in next_neigy:
        if type(agent) is Coche:

          self.length = 1
          self.waiting_time += 1
          self.can_move = False

        if type(agent) is Semaforo:
          if next_neigy[0].light == 0:

            self.can_move = False
            self.waiting_time += 1


          elif next_neigy[0].light == 1:

            self.model.grid.move_agent(self, nexty)



    self.move()

  def step(self):
    self.vecinos()


class Calle(Model):
  def __init__(self, height = 13, width = 13, no = 2):
    self.height = height
    self.width = width
    self.no = no
    self.schedule = RandomActivationByBreed(self)
    self.grid = MultiGrid(self.height, self.width, torus = True)
    self.running = True



    for i in range (0,1):
      x = 0
      y = 5
      length = 0
      can_move = False
      waiting_time = 0
      orientation = 0
      coche = Coche((x,y), self, False, length, can_move, waiting_time, orientation)
      self.grid.place_agent(coche, (x,y))
      self.schedule.add(coche)

    for i in range (0,1):
      x = 3
      y = 5
      length = 0
      can_move = False
      waiting_time = 0
      orientation = 0
      coche = Coche((x,y), self, False, length, can_move, waiting_time, orientation)
      self.grid.place_agent(coche, (x,y))
      self.schedule.add(coche)


    for i in range (0,1):
      x = 6
      y = 11
      length = 0
      can_move = False
      waiting_time = 0
      orientation = 1
      coche = Coche((x,y), self, False, length, can_move, waiting_time, orientation)
      self.grid.place_agent(coche, (x,y))
      self.schedule.add(coche)





    for i in range(0,1):
      x = 5
      y = 5
      light = 0
      working_time = 0
      orientation = 0

      light =  Semaforo((x,y), self, False, light, working_time, orientation)
      self.grid.place_agent(light, (x,y))
      self.schedule.add(light)

    for i in range(0,1):
      x = 6
      y = 6
      light = 0
      working_time = 0
      orientation = 1

      light =  Semaforo((x,y), self, False, light, working_time, orientation)
      self.grid.place_agent(light, (x,y))
      self.schedule.add(light)


    for i in range(0, 5):
      x = 0 + i
      y = 6

      orientation = 0
      banqueta = Banquetas((x,y), self, False, orientation)
      self.grid.place_agent(banqueta, (x,y))
      self.schedule.add(banqueta)

    for i in range(8, 12):
      x = 0 + i
      y = 6

      orientation = 0
      banqueta = Banquetas((x,y), self, False, orientation)
      self.grid.place_agent(banqueta, (x,y))
      self.schedule.add(banqueta)

    for i in range(0, 5):
      x = 0 + i
      y = 4
      orientation = 0
      banqueta = Banquetas((x,y), self, False, orientation)
      self.grid.place_agent(banqueta, (x,y))
      self.schedule.add(banqueta)

    for i in range(8, 12):
      x = 0 + i
      y = 4
      orientation = 0
      banqueta = Banquetas((x,y), self, False, orientation)
      self.grid.place_agent(banqueta, (x,y))
      self.schedule.add(banqueta)

    for i in range(0, 4):
      x = 5
      y = 0 + i
      orientation = 1
      banqueta = Banquetas((x,y), self, False, orientation)
      self.grid.place_agent(banqueta, (x,y))
      self.schedule.add(banqueta)

    for i in range(0, 4):
      x = 7
      y = 0 + i
      orientation = 1
      banqueta = Banquetas((x,y), self, False, orientation)
      self.grid.place_agent(banqueta, (x,y))
      self.schedule.add(banqueta)

    for i in range(7, 13):
      x = 7
      y = 0 + i
      orientation = 1
      banqueta = Banquetas((x,y), self, False, orientation)
      self.grid.place_agent(banqueta, (x,y))
      self.schedule.add(banqueta)

    for i in range(7, 13):
      x = 5
      y = 0 + i
      orientation = 1
      banqueta = Banquetas((x,y), self, False, orientation)
      self.grid.place_agent(banqueta, (x,y))
      self.schedule.add(banqueta)


  def step(self):

    self.schedule.step()

  def getCoche(self):
      c = []
      for n in self.schedule.agents:
          if isinstance(n, Coche):
              c.append({"id": n.unique_id, "pos":[n.pos[0], n.pos[1]], "l": n.length, "m": n.can_move, "w": n.waiting_time, "o": n.orientation})
      return c

  def getSemaforo(self):
      s = []
      for n in self.schedule.agents:
          if isinstance(n, Semaforo):
              s.append({"id": n.unique_id, "pos":[n.pos[0], n.pos[1]], "l": n.light, "w": n.working_time, "o": n.orientation})
      return s

  def getBanquetas(self):
      b = []
      for n in self.schedule.agents:
          if isinstance(n, Banquetas):
              b.append({"id": n.unique_id, "pos":[n.pos[0], n.pos[1]], "o": n.orientation})
      return b

def agent_portrayal(agent):


  portrayal = {}

  if type(agent) is Coche:

    if agent.orientation == 0:
      return{"Shape":"resources/OIP.jpg","Scale":.5,"Layer": "Coche"}


    if agent.orientation == 1:
      return{"Shape":"resources/OI.jpg","Scale":.9,"Layer": "Coche"}

  if type(agent) is Semaforo:
    return{"Shape":"resources/s.jpg","Scale":.5,"Layer": "Light"}

  if type(agent) is Banquetas:

    if agent.orientation == 0:
      return{"Shape":"resources/b.jpg","Scale":.25,"Layer": "Sidewalk"}

    elif agent.orientation == 1:
      return{"Shape":"resources/b.jpg","Scale":.15,"Layer": "Sidewalk"}




  return portrayal


grid = CanvasGrid(agent_portrayal, 13, 13, 500, 500)


server = ModularServer(
    Calle, [grid], " Test"
)

server.port = int(os.getenv('PORT', 8000))
# server.port = 8522 #
server.launch()
