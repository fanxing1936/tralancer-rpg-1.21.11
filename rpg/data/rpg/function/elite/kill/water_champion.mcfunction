# 玩家打死了首领精英（as/at 玩家）
advancement revoke @s only rpg:elite/kill_water_champion
loot give @s loot rpg:elite/water_champion
scoreboard players add @s rpg_el_kill 1
scoreboard players add @s rpg_ex_xp 15
playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 0.6 1.4
playsound minecraft:entity.player.levelup player @s ~ ~ ~ 0.5 1.6
loot give @s loot rpg:world/elite_extra/water_champion
execute if entity @s[y=-64,dy=63] if predicate {condition:"minecraft:random_chance",chance:0.25} run loot give @s loot rpg:world/sp/stone
execute if score @s rpg_el_kill matches 100 run function rpg:world/kab/give_victory
function rpg:events/e1/champ
function rpg:events/bt/elite
function rpg:quest/hook/elite
execute if entity @s[tag=rpg.pl.in] run loot give @s loot rpg:paradise/champ
execute if entity @s[tag=rpg.pl.in] run function rpg:events/bt/paradise_champ
execute if entity @s[tag=rpg.pl.in] if score #rain rpg_pl matches 1.. run loot give @s loot rpg:paradise/rain_champ
execute if predicate {condition:"minecraft:random_chance",chance:0.1} run loot give @s loot rpg:potion/any_epic
function rpg:paths/champ
execute if score @s rpg_ps_21 matches 3 if predicate {condition:"minecraft:random_chance",chance:0.1} run loot give @s loot rpg:elite/water_champion
