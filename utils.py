import os
import html_parser
import pickle

class Utils:
	@staticmethod
	def getAllSkills(dir = "./resources/skill/"):
		skills = []
		for f in os.listdir(dir):
			fpath = os.path.join(dir, f)
			sp = html_parser.SkillParser(fpath)
			skills.extend(sp.getSkills())
		skfile = open('./resources/skill/skill.pickle', 'wb')
		pickle.dump(skills, skfile)
	
	@staticmethod
	def levenshteinDistance(string1, string2):
		len1, len2 = len(string1), len(string2)
		if len1 > len2:
			string1, string2 = string2, string1
			len1, len2 = len2, len1

		current = range(len1 + 1)
		for i in range(1, len2 + 1):
			previous, current = current, [i] + [0] * len1
			for j in range(1, len1 + 1):
				add, delete = previous[j] + 1, current[j - 1]+1
				change = previous[j-1]
				if string1[j - 1] !=string2[i - 1]:
					change = change+1
				current[j] = min(add, delete, change)
		return current[len1]

if __name__ == '__main__':
	print Utils.levenshteinDistance('abc', 'abd')