from abc import ABCMeta, abstractmethod

class Menu:
	__metaclass__ = ABCMeta

	@abstractmethod
	def run(self): pass