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
class CustomerAgent:
    def __init__(self, x:float, y:float):
        # エージェントの初期位置
        self.x:float = x
        self.y:float = y


    def move(self, obstacles, other_agents, width:int, height:int):
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
        self.x, self,y = new_x, new_y

