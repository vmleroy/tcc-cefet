package thread;

import engine.core.MarioGame;
import engine.core.MarioResult;

public class GameRunnable implements Runnable {

  private String level = null;
  private Integer timer = 60;
  private Integer marioState = 0;
  private MarioResult result;

  public void setLevel(String level) {
    this.level = level;
  }

  public void setTimer(Integer timer) {
    this.timer = timer;
  }

  public void setMarioState(Integer marioState) {
    this.marioState = marioState;
  }

  public MarioResult getResult() {
    return this.result;
  }

  @Override
  public void run() {
    if (this.level == null) {
      return;
    }

    MarioGame game = new MarioGame();
    this.result = game.runGame(new agents.robinBaumgarten.Agent(), this.level, this.timer, this.marioState);
  }
}