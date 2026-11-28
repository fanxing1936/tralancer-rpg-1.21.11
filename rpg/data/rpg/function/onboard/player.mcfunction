# 流程中的玩家每刻（as/at 玩家；序章里的人不走这里）
execute if score @s rpg_ob_lv matches 1.. run function rpg:onboard/relog
scoreboard players add @s rpg_ob_t 1
scoreboard players enable @s rpg_ob_do
execute if score @s rpg_ob_do matches 1.. run function rpg:onboard/press
# 停在序章这一步却没在排队、也没分到战场（比如老存档）：排进去
execute if score @s rpg_ob matches 1 unless entity @s[tag=rpg.ob.fin] unless entity @s[tag=rpg.pr.q] unless score @s rpg_pr_g matches 1.. run function rpg:prologue/enqueue
# 序章打完、回到原处：等一秒、脚下的区块载入了再进正式游戏（还装备要在这里召临时实体）
execute if entity @s[tag=rpg.ob.fin] if score @s rpg_ob_t matches 20.. if loaded ~ ~ ~ run function rpg:onboard/pro/fin
execute if entity @s[tag=rpg.ob.wait] if score @s rpg_ob_t matches 60.. run function rpg:onboard/show
execute if entity @s[tag=rpg.ob.intro] run function rpg:onboard/intro/tick
execute if score @s rpg_ob_mi matches 1.. run function rpg:onboard/music/tick
scoreboard players operation #m rpg_ob = @s rpg_ob_t
scoreboard players operation #m rpg_ob %= #twenty rpg_ob
execute if score #m rpg_ob matches 0 run function rpg:onboard/hold/keep
