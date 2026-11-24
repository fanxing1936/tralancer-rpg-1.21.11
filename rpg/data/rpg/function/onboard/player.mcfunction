# 流程中的玩家每刻（as/at 玩家；序章里的人不走这里）
execute if score @s rpg_ob_lv matches 1.. run function rpg:onboard/relog
scoreboard players add @s rpg_ob_t 1
scoreboard players enable @s rpg_ob_do
execute if score @s rpg_ob_do matches 1.. run function rpg:onboard/press
execute if score @s rpg_ob matches 1 unless entity @s[tag=rpg.ob.pro] if score @s rpg_ob_t matches 100.. run function rpg:onboard/pro/try
execute as @s[tag=rpg.ob.queued] unless score @s rpg_ob matches 1 run tag @s remove rpg.ob.queued
# 序章在准备阶段就取消了（没把人接进去）：跳过序章
execute if entity @s[tag=rpg.ob.pro] if score @s rpg_ob_t matches 100.. unless score #state rpg_pr matches 1.. run function rpg:onboard/pro/after
execute if entity @s[tag=rpg.ob.wait] if score @s rpg_ob_t matches 60.. run function rpg:onboard/show
execute if entity @s[tag=rpg.ob.intro] run function rpg:onboard/intro/tick
execute if score @s rpg_ob_mi matches 1.. run function rpg:onboard/music/tick
scoreboard players operation #m rpg_ob = @s rpg_ob_t
scoreboard players operation #m rpg_ob %= #twenty rpg_ob
execute if score #m rpg_ob matches 0 run function rpg:onboard/hold/keep
