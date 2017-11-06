from copy import deepcopy
from enum import Enum

from gym import Env
from gym.spaces import Box


class Action(Enum):
    UP = (0, 1)
    DOWN = (0, -1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


class Tile(Enum):
    AGENT = 'A'
    EMPTY = ' '
    WALL = 'W'
    TARGET = '*'


default_grid_str = """
WWWWWWWWWWWWW
W     W     W
W  A  W     W
W           W
W     W     W
W     W     W
WW WWWW     W
W     WWW WWW
W     W     W
W     W     W
W         * W
W     W     W
WWWWWWWWWWWWW
"""


class FourRoomEnv(Env):
    action_space = [action.value for action in Action]
    observation_space = Box(0, 5)  # TODO: not sure

    def __init__(self, agent_location=[0, 0], target_location=[0, 0], grid_str=default_grid_str):
        self.initial_grid = [list(s) for s in grid_str.strip().split('\n')]
        self.M, self.N = len(self.grid[0]), len(self.grid)
        self.initial_agent_location = next(
            (i, j)
            for j in range(self.M)
            for i in range(self.N)
            if self.initial_grid[i][j] == 'A')
        self.initial_target_location = next(
            (i, j)
            for j in range(self.M)
            for i in range(self.N)
            if self.initial_grid[i][j] == '*')

        self._reset()

    def _seed(self):
        """Sets the seed for this env's random number generator(s).
        Note:
            Some environments use multiple pseudorandom number generators.
            We want to capture all such seeds used in order to ensure that
            there aren't accidental correlations between multiple generators.
        Returns:
            list<bigint>: Returns the list of seeds used in this env's random
              number generators. The first value in the list should be the
              "main" seed, or the value which a reproducer should pass to
              'seed'. Often, the main seed equals the provided 'seed', but
              this won't be true if seed=None, for example.
        """
        return []

    def _step(self, action):
        """Run one timestep of the environment's dynamics. When end of
        episode is reached, you are responsible for calling `reset()`
        to reset this environment's state.
        Accepts an action and returns a tuple (observation, reward, done, info).
        Args:
            action (object): an action provided by the environment
        Returns:
            observation (object): agent's observation of the current environment
            reward (float) : amount of reward returned after previous action
            done (boolean): whether the episode has ended, in which case further step() calls will return undefined results
            info (dict): contains auxiliary diagnostic information (helpful for debugging, and sometimes learning)
        """
        assert(isinstance(action, Action))
        next_agent_location = (self.agent_location[0] + action.value[0], self.agent_location[1] + action.value[1])
        if next_agent_location[0] < 0 or next_agent_location[0] >= self.M or next_agent_location[1] < 0 or next_agent_location[1] >= self.N or self.grid[next_agent_location] == Tile.WALL.value:
            return (self.agent_location, 0, False, None)
        else:
            self.grid[self.agent_location[0]][self.agent_location[1]] = Tile.EMPTY
            self.agent_location = next_agent_location
            self.grid[self.agent_location[0]][self.agent_location[1]] = Tile.AGENT
            return (self.agent_location, 1, self.agent_location == self.target_location, None)

    def _reset(self):
        """Resets the state of the environment and returns an initial observation.
        Returns: observation (object): the initial observation of the
            space.
        """
        self.agent_location = self.initial_agent_location
        self.target_location = self.initial_target_location
        self.grid = deepcopy(self.initial_grid)

    def _render(self, mode='human', close=False):
        """Renders the environment.
        The set of supported modes varies per environment. (And some
        environments do not support rendering at all.) By convention,
        if mode is:
        - human: render to the current display or terminal and
          return nothing. Usually for human consumption.
        - rgb_array: Return an numpy.ndarray with shape (x, y, 3),
          representing RGB values for an x-by-y pixel image, suitable
          for turning into a video.
        - ansi: Return a string (str) or StringIO.StringIO containing a
          terminal-style text representation. The text can include newlines
          and ANSI escape sequences (e.g. for colors).
        Note:
            Make sure that your class's metadata 'render.modes' key includes
              the list of supported modes. It's recommended to call super()
              in implementations to use the functionality of this method.
        Args:
            mode (str): the mode to render with
            close (bool): close all open renderings
        Example:
        class MyEnv(Env):
            metadata = {'render.modes': ['human', 'rgb_array']}
            def render(self, mode='human'):
                if mode == 'rgb_array':
                    return np.array(...) # return RGB frame suitable for video
                elif mode is 'human':
                    ... # pop up a window and render
                else:
                    super(MyEnv, self).render(mode=mode) # just raise an exception
        """
        if mode == 'human':
            print(self.grid)
        else:
            print('NOT YET IMPLEMENTED')
