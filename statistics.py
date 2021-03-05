import matplotlib.pyplot as plt

plt.ion()

def plot(scores, mean):
  plt.clf()
  plt.title('Statistics')
  plt.xlabel('Games')
  plt.ylabel('Score')
  plt.plot(scores)
  plt.plot(mean)
  plt.ylim(ymin=0)
  plt.text(len(scores)-1, scores[-1], str(scores[-1]))
  plt.text(len(mean)-1, mean[-1], str(mean[-1]))
  plt.pause(0.0001)
  plt.show()

