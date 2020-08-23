# Rock-Paper-Scissors game with your computer ✌
Rock-paper-scissors game with computer. The thumb sign ends the game.

I used <a href="https://github.com/tensorflow/models/tree/master/research/object_detection"> Tensorflow 2.x.0 Object Detection API </a> to recognize 5 different gestures, preicisely the *SSD_mobilenet_v2* pre-trained model.

The files used for training you can find <a href="https://github.com/weronikazak/AI-rock-paper-scissors/tree/master/tensorflow_object_detection_api" target="_blank">here</a>. By modyfying the `hand_track.py` file you will be able to test the trained model's on your own. Make sure you have enabled your camera.

I tried to use Oxford's hands dataset, but it failed at detecting my hands. So I made my own. It cnsists of ~700 images in environment with different level of lightings.

Big thanks for *tzutalin* for his handy tool <a href="https://github.com/tzutalin/labelImg"> labelImg</a>.


Trained on 5 different gestures:
- Peace (V) sign - Scissors sign
- Fist - Rock sign
- Straight hand or Five - Paper sign
- Thumb left - Quit sign
- Other


## Performance:

<p align="center">
  <img src="https://github.com/weronikazak/AI-rock-paper-scissors/blob/master/examples/loss.PNG">
</p>

Although the loss function looks pretty good, the detector behaves chaotic at times, e. g. detecting a face instead of a hand. I think that expanding the dataset and making it more various in terms of lighting and surrounding will solve that problem.

<p align="center">
  <img src="https://github.com/weronikazak/AI-rock-paper-scissors/blob/master/examples/round.gif">
</p>

<b>Find more examples <a href="https://github.com/weronikazak/AI-rock-paper-scissors/tree/master/examples">here</a>.</b>



-------



## TO DO:

- [ ] Retrain model to recognize only four gestures (rock, scissors, paper, quit sign).

- [ ] Change the quit sign to a different gesture.

- [ ] Design better GUI.

- [ ] Add more data in different surroundings with different lightings.
