advancement revoke @s only rpg:paradise/kill_z1
scoreboard players add @s rpg_pl_kill 1
loot give @s loot rpg:paradise/z1
execute if score #moon rpg_pl matches 1.. run loot give @s loot rpg:paradise/z1
execute if score #rain rpg_pl matches 1.. run loot give @s loot rpg:paradise/rain_z1
function rpg:events/bt/paradise
