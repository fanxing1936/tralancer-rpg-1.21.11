scoreboard players operation #do rpg_q_st = @s rpg_q_do
scoreboard players set @s rpg_q_do 0
scoreboard players enable @s rpg_q_do
execute if score #do rpg_q_st matches 1 run return run function rpg:quest/titles
execute if score #do rpg_q_st matches 20 if entity @s[tag=rpg.q1.pick] run loot give @s loot rpg:world/bp/dark_sun
execute if score #do rpg_q_st matches 21 if entity @s[tag=rpg.q1.pick] run loot give @s loot rpg:world/bp/chainsaw
execute if score #do rpg_q_st matches 22 if entity @s[tag=rpg.q1.pick] run loot give @s loot rpg:world/bp/earth_spine
execute if score #do rpg_q_st matches 23 if entity @s[tag=rpg.q1.pick] run loot give @s loot rpg:world/bp/venom_fang
execute if score #do rpg_q_st matches 24 if entity @s[tag=rpg.q1.pick] run loot give @s loot rpg:world/bp/wind_bone
execute if score #do rpg_q_st matches 25 if entity @s[tag=rpg.q1.pick] run loot give @s loot rpg:world/bp/mischief_bow
execute if score #do rpg_q_st matches 26 if entity @s[tag=rpg.q1.pick] run loot give @s loot rpg:world/bp/vine_whip
execute if score #do rpg_q_st matches 27 if entity @s[tag=rpg.q1.pick] run loot give @s loot rpg:world/bp/truth_blade
execute if score #do rpg_q_st matches 28 if entity @s[tag=rpg.q1.pick] run loot give @s loot rpg:world/bp/crystal_roar
execute if score #do rpg_q_st matches 40 run function rpg:quest/title/wear_gate
execute if score #do rpg_q_st matches 41 run function rpg:quest/title/wear_ledger
execute if score #do rpg_q_st matches 42 run function rpg:quest/title/wear_waverer
execute if score #do rpg_q_st matches 43 run function rpg:quest/title/wear_grandmaster
execute if score #do rpg_q_st matches 44 run function rpg:quest/title/wear_meteor
execute if score #do rpg_q_st matches 45 run function rpg:quest/title/wear_merchant
execute if score #do rpg_q_st matches 46 run function rpg:quest/title/wear_summit
execute if score #do rpg_q_st matches 47 run function rpg:quest/title/wear_sever
execute if score #do rpg_q_st matches 48 run function rpg:quest/title/wear_mirror
execute if score #do rpg_q_st matches 20..28 run tag @s remove rpg.q1.pick
execute if score #do rpg_q_st matches 49 run function rpg:quest/title/off
