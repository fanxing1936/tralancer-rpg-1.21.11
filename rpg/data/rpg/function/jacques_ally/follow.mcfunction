# 没有敌人：跟着召唤他的人（离开 4 格以上就走过去，远过 24 格直接跟上）。
scoreboard players operation #own rpg_al = @s rpg_al_own
execute as @a if score @s rpg_al_id = #own rpg_al run tag @s add rpg.al.me
execute if entity @a[tag=rpg.al.me,distance=24..] at @a[tag=rpg.al.me,limit=1] run tp @s ~ ~ ~
execute unless entity @a[tag=rpg.al.me,distance=..4] facing entity @a[tag=rpg.al.me,limit=1] feet rotated ~ 0 run function rpg:jacques_ally/step
tag @a remove rpg.al.me
