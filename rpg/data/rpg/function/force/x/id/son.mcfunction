function rpg:force/unholy
execute unless score #u rpg_fo matches 1 run return 0
scoreboard players add #pct rpg_fo 25
execute if entity @a[tag=rpg.fo.me,limit=1,scores={rpg_sef=5..}] run scoreboard players add #pct rpg_fo 25
