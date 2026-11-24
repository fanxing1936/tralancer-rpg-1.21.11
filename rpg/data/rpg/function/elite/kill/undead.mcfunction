# 玩家打死了精英（as/at 玩家）
advancement revoke @s only rpg:elite/kill_undead
loot give @s loot rpg:elite/undead
scoreboard players add @s rpg_el_kill 1
playsound minecraft:entity.player.levelup player @s ~ ~ ~ 0.5 1.6
loot give @s loot rpg:world/elite_extra/undead
execute if score @s rpg_el_kill matches 100 run function rpg:world/kab/give_victory
function rpg:events/bt/elite
function rpg:quest/hook/elite
