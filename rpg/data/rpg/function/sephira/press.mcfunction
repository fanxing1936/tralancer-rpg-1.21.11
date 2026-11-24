scoreboard players operation #do rpg_sef = @s rpg_sef_do
scoreboard players set @s rpg_sef_do 0
execute if score #do rpg_sef matches 1 run function rpg:sephira/pillar/set_1
execute if score #do rpg_sef matches 2 run function rpg:sephira/pillar/set_2
execute if score #do rpg_sef matches 3 run function rpg:sephira/pillar/set_3
execute if score #do rpg_sef matches 9 run function rpg:sephira/pillar/ask
execute if score #do rpg_sef matches 11 run function rpg:sephira/force/awaken_1
execute if score #do rpg_sef matches 12 run function rpg:sephira/force/awaken_2
execute if score #do rpg_sef matches 19 run function rpg:sephira/force/awaken_ask
execute if score #do rpg_sef matches 20 run function rpg:sephira/page/open
execute if score #do rpg_sef matches 21 if entity @s[tag=rpg.fallen] if score @s rpg_lt_divine matches 2 run function rpg:sephira/force/rise
