# 退书 + 解约。逆圣化与毁约两条路共用这一段。
#
# 顺序要紧：先把书退回未立约，再 break —— break 会清掉柱位编号，
# 清掉之后就认不出该退成哪一本了。
execute if entity @s[scores={rpg_pact=1}] run function rpg:pact/unsign1
execute if entity @s[scores={rpg_pact=2}] run function rpg:pact/unsign2
execute if entity @s[scores={rpg_pact=3}] run function rpg:pact/unsign3
execute if entity @s[scores={rpg_pact=4}] run function rpg:pact/unsign4
execute if entity @s[scores={rpg_pact=5}] run function rpg:pact/unsign5
execute if entity @s[scores={rpg_pact=6}] run function rpg:pact/unsign6
execute if entity @s[scores={rpg_pact=7}] run function rpg:pact/unsign7
function rpg:pact/break
