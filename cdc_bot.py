#!/usr/bin/env python
#-*- coding: utf-8 -*-
import logging
logging.basicConfig(level=logging.DEBUG)
import discord
client = discord.Client()
from game import Game, Combinations

def in_game(f):
	"""Decorator: only process if the game is initialised"""
	def newfunc(bot, line):
		if bot.game:
			return f(bot, line)
	return newfunc
def in_running_game(f):
	"""Decorator: only process if the game is running"""
	def newfunc(bot, line):
		if bot.game and bot.game.started:
			return f(bot, line)
	return newfunc
def not_in_special_rule(f):
	"""Decorator: do not process if the game is in a special rule case"""
	def newfunc(bot, line):
		if not bot.game.in_special_rule:
			return f(bot, line)
	return newfunc

async def say_discord(channel, msg):
	await client.send_message(channel, msg)

class CulDeChouetteBot():

	async def say(self, discord, message):
		await say_discord(discord.channel, message)

	def game(self):
		if not hasattr(self, '_game'):
			self._game = Game()
		return self._game

	async def do_init(self, line):
		""""Initialise a game"""
		logging.info('ici')
		if hasattr(self, 'game') and hasattr(self.game, 'started') and self._game.started:
			await self.say(line, "Non, on ne peut pas.")
			return

		await self.say(line, 'Le jeu est prêt à commencer')
		await self.say(line, 'Qui veut jouer ? (dire "!qdc moi")')

	async def do_start(self, line):
		"""Start the game"""
		#if len(self._game.gamers) < 3:
		#	await self.say(line, 'Pas assez de joueurs. Inscrivez-vous en disant "!qdc moi"')
		#	return
		self._game.start()
		await self.say(line, 'Ça démarre... qui commence ?...')
		await self.say(line, "c'est au tour de '%s'" % self._game.current_gamer)

	async def do_scores(self, line):
		"""Say the gamer list, with scores"""
		s = []
		for nick, score in self._game.gamers.items():
			s.append('%s (%d)' % (nick, score))
		await self.say(line, 'Joueurs: %s' % ', '.join(s))

	async def do_moi(self, line):
		"""Register the user"""
		if line.author not in self._game.gamers:
			self._game.gamers[line.author] = 0
			await self.say(line, '%s est inscrit' % line.author)
		else:
			await self.say(line, 'déjà inscrit...')

	async def do_roll(self, line):
		"""Roll the dice if it's your turn"""
		if line.author == self._game.current_gamer:
			dices = self._game.dices()
			await self.say(line, 'Les dés: %s' % ', '.join(map(str, dices)))
			c = Combinations(dices)
			score, messages, is_suite = c.resultat()
			for message in messages:
				await self.say(line, message)
			if is_suite:
				self._game.in_suite = True
				self._game.grelotte = []
				return  # nothing else to do ATM
			if score > 0:
				await self.say(line, '%s gagne %d points' % (line.author, score))
				self._game.gamers[line.author] += score

			if self._game.gamers[line.author] >= 343:
				await self.say(line, "Le jeu est terminé ! C'est *%s* qui a gagné !" % str(line.author))
				self._game.stop()
				return

			self._game.next()
			await self.say(line, "c'est au tour de '%s'" % self._game.current_gamer)
		else:
			await self.say(line, "C'est pas ton tour, manant !")

	async def do_grelotte(self, line):
		"""Grelotte ca picote"""
		if self._game.in_suite:
			grelotte_line = ' '.join(line.message.split())
			if grelotte_line.startswith(u'grelotte ça picote') \
					or grelotte_line.startswith(u'grelotte ca picote'):
				if line.author not in self._game.grelotte:
					self._game.grelotte.append(line.author)
			# check if everyone's here
			difference = list(set(self._game.gamers.keys()).difference(set(self._game.grelotte)))
			if len(difference) == 1:
				gamer_nick = difference[0]
				await self.say(line, '%s perd 10 points' % (gamer_nick))
				self._game.gamers[gamer_nick] -= 10
				self._game.next()
				await self.say(line, "c'est au tour de '%s'" % self._game.current_gamer)

		else:
			# TODO: handle bevue
			await self.say(line, 'Bévue !')

	async def do_stop(self, line):
		"Stop the current game"
		await self.say(line, 'Le jeu est arrêté')
		self._game.stop()

	async def do_status(self, line):
		"Give the current game status"
		if not self._game.started:
			await self.say(line, 'Aucun jeu en cours')
			return
		self.do_scores(line)
		await self.say(line, "C'est le tour de : %s" % self._game.current_gamer)


bot = CulDeChouetteBot()
bot.game()

@client.event
async def on_message(message):
	if message.author == client.user:
		return

	if message.content.startswith('!qdc init'):
		say_discord(message.channel, "Salut la compagnie ! Ça vous dirait un cul-de-chouette ?")
		await bot.do_init(message)
	
	if message.content.startswith('!qdc start'):
		await bot.do_start(message)
	
	if message.content.startswith('!qdc stop'):
		await bot.do_stop(message)

	if message.content.startswith('!qdc scores'):
		await bot.do_scores(message)
	
	if message.content.startswith('!qdc moi'):
		await bot.do_moi(message)
	
	if message.content.startswith('!qdc roll'):
		await bot.do_roll(message)
	
	if message.content.startswith('!qdc grelotte'):
		await bot.do_grelotte(message)
	
	if message.content.startswith('!qdc status'):
		await bot.do_status(message)


@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')

client.run('Discord bot key')
