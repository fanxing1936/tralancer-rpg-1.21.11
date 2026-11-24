advancement revoke @s only rpg:paradise/kill_z3
scoreboard players add @s rpg_pl_kill 1
loot give @s loot rpg:paradise/z3
execute if score #moon rpg_pl matches 1.. run loot give @s loot rpg:paradise/z3
function rpg:events/bt/paradise
