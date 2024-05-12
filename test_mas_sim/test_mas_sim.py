"""
# MAS
## MASとは
複数のエージェントを用いたシミュレーションのこと．
## MASの考え方
シミュレーション環境上にエージェントを多数配置し，それらは与えられた行動基準に従って相互作用を繰り返す．
その結果としてシミュレーション環境全体に生じた大きな現象やプロセスを確認する．
## エージェントの定義
自分の周囲の状況を認識し，それに基づいて一定のルールで自律的に行動する主体．
## シミュレーションの定義
現実を模したモデルを用いて予測や分析を行う．
"""
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation


"""
# エージェントの基本的な原則とメカニズム
## エージェントの特性
エージェントには以下のような特性をもたせる．
- 自立性:       エージェントは独立して行動．自らの判断でタスクを実行する．
- 局所的な知識: 各エージェントの全体の情報は持たない．自身の周囲の情報をもとに行動を行う．
- 多様性:       エージェントは異なる特性やルールを持てる．
## エージェントの行動原則のモデリング
以下の行動原則に従ってエージェントのモデリングを行う．
- ルールベースの行動:   エージェントは予め設定されたルールやアルゴリズムに沿って行動する．
- 学習と適応:           一部のエージェントは，環境からのフィードバックを通じて学習が可能であり，行動を適応することが可能である．
"""
############################################################
# エージェントの定義
############################################################
# - エージェントの進み方，障害物やほかのエージェントと衝突
#   した場合など，動きに関する行動ルールを定義する．
# - エージェントは前か右へ0.5進むか静止するように行動を定義
############################################################
class CustomerAgent:
    def __init__(self, x:float, y:float):
        # エージェントの初期位置
        self.x:float = x
        self.y:float = y


    def move(self, obstacles, other_agents, width:int, height:int) -> None:
        # 新しいエージェントの位置を決定
        new_x:float = self.x + random.choice([0, 0.5])
        new_y:float = self.y + random.choice([0, 0.5])

        # 店の境界の確認
        if new_x < 0 or new_x >= width:
            return # 移動なし
        if new_y < 0 or new_y >= height:
            return # 移動なし

        # 障害物や他のエージェントとの衝突確認
        for obs in obstacles:
            # エージェントが障害物と衝突する時
            if new_x == obs[0] and new_y == obs[1]:
                return # 移動なし
        for agent in other_agents:
            # エージェントがほかのエージェントと衝突する時
            if new_x == agent.x and new_y == agent.y:
                return # 移動しない

        # 移動を更新
        self.x, self.y = new_x, new_y


"""
# 環境のモデリング
## 環境のモデリングの要素
- インタラクティブな環境: エージェントは，仮想環境内で操作される．この環境はエージェントに影響を与え，その反応によって変化することがある．
- リアルタイムな動的変化: 環境は時間と共に変化する．エージェントの行動にも影響を受ける．
"""
############################################################
# エージェントの定義
############################################################
# - 店の広さや障害物の設定などシミュレーション環境の定義を
#   行う
# - エージェントは最初左下に位置し，入店する．
#   中央に商品だなを設置する，
############################################################
class Sim:
    def __init__(self, store_width:int, store_height:int, num_agent:int, obstacles:list, num_steps:int):
        self.store_width:int = store_width      # 店の横幅
        self.store_height:int = store_height    # 店の奥行き
        self.position_over_time:list = []

        self.obstacles:list = obstacles

        # エージェントの初期位置設置と生成
        self.ca = CustomerAgent(1, 1)
        self.agents:list = [ CustomerAgent(1, 1) for _ in range(num_agent) ]

        self.num_steps:int = num_steps

        # アニメーションの設定
        self.fig, self.ax = plt.subplots(figsize=(5, 5))


    def update_positions(self, width:int, height:int) -> list:
        for agent in self.agents:
            agent.move(self.obstacles, [ a for a in self.agents if a != agent ], width, height)

        return [ (agent.x, agent.y) for agent in self.agents ]


    def run_sim(self) -> None:
        for step in range(self.num_steps):
            positions = self.update_positions(self.store_width, self.store_height)
            self.position_over_time.append(positions)


    def animate_sim(self, step:int) -> None:
        self.ax.clear()
        self.ax.set_xlim(0, self.store_width)
        self.ax.set_ylim(0, self.store_height)
        x_values, y_values = zip(*self.position_over_time[step])
        self.ax.scatter(x_values, y_values, label='Customers')
        obs_x, obs_y = zip(*self.obstacles)
        self.ax.scatter(obs_x, obs_y, color='red', marker=',', label='Obstacles')
        self.ax.legend()
        self.ax.set_title(f'Step {step}')


    def app(self, f_path:str, save_mov:bool) -> None:
        ani = animation.FuncAnimation(self.fig, self.animate_sim, frames=self.num_steps, repeat=False)
        plt.show()
        if save_mov:
            ani.save(f_path, writer='imagemagick', fps=1)


if __name__ == '__main__':
    num_agent:int = 10
    obstacles:list = [(5,5), (5.5, 5), (6, 5), (5, 6), (5.5, 6), (6,6)]    # 障害物の設定, 店の中央に配置
    num_steps:int = 50
    sim = Sim(10, 10, num_agent, obstacles, num_steps)
    sim.run_sim()
    sim.app('./result.gif', True)
