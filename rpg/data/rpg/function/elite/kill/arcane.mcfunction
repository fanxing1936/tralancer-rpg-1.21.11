# 玩家打死了精英（as/at 玩家）
advancement revoke @s only rpg:elite/kill_arcane
loot give @s loot rpg:elite/arcane
scoreboard players add @s rpg_el_kill 1
playsound minecraft:entity.player.levelup player @s ~ ~ ~ 0.5 1.6
loot give @s loot rpg:world/elite_extra/arcane
execute if score @s rpg_el_kill matches 100 run function rpg:world/kab/give_victory
function rpg:events/bt/elite
function rpg:quest/hook/elite
execute if entity @s[tag=rpg.pl.in] if score #rain rpg_pl matches 1.. run loot give @s loot rpg:paradise/rain_elite
execute if score @s rpg_ps_21 matches 3 if predicate {condition:"minecraft:random_chance",chance:0.1} run loot give @s loot rpg:elite/arcane
