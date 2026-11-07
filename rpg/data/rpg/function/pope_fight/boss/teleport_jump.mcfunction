# 瞬移打断加护，落点在最近玩家周围 13.5 格。
effect clear @e[type=minecraft:vindicator,tag=rpg.pf.unit] minecraft:resistance
particle flash{color:16773800} ~ ~1 ~ 0 0 0 0 1 normal
particle end_rod ~ ~1 ~ 0.4 0.8 0.4 0.05 24 normal
execute positioned ~ ~1.3 ~ run function rpg:pope_fight/fx/ring
execute store result score #r rpg_pf run random value 0..7
execute if score #r rpg_pf matches 0 at @a[distance=..48,gamemode=!spectator,gamemode=!creative,sort=nearest,limit=1] positioned ~13.5 ~ ~0.0 positioned over motion_blocking_no_leaves facing entity @a[distance=..16,gamemode=!spectator,gamemode=!creative,sort=nearest,limit=1] feet rotated ~ 0 run tp @s ~ ~ ~ ~ 0
execute if score #r rpg_pf matches 1 at @a[distance=..48,gamemode=!spectator,gamemode=!creative,sort=nearest,limit=1] positioned ~9.5 ~ ~9.5 positioned over motion_blocking_no_leaves facing entity @a[distance=..16,gamemode=!spectator,gamemode=!creative,sort=nearest,limit=1] feet rotated ~ 0 run tp @s ~ ~ ~ ~ 0
execute if score #r rpg_pf matches 2 at @a[distance=..48,gamemode=!spectator,gamemode=!creative,sort=nearest,limit=1] positioned ~0.0 ~ ~13.5 positioned over motion_blocking_no_leaves facing entity @a[distance=..16,gamemode=!spectator,gamemode=!creative,sort=nearest,limit=1] feet rotated ~ 0 run tp @s ~ ~ ~ ~ 0
execute if score #r rpg_pf matches 3 at @a[distance=..48,gamemode=!spectator,gamemode=!creative,sort=nearest,limit=1] positioned ~-9.5 ~ ~9.5 positioned over motion_blocking_no_leaves facing entity @a[distance=..16,gamemode=!spectator,gamemode=!creative,sort=nearest,limit=1] feet rotated ~ 0 run tp @s ~ ~ ~ ~ 0
execute if score #r rpg_pf matches 4 at @a[distance=..48,gamemode=!spectator,gamemode=!creative,sort=nearest,limit=1] positioned ~-13.5 ~ ~0.0 positioned over motion_blocking_no_leaves facing entity @a[distance=..16,gamemode=!spectator,gamemode=!creative,sort=nearest,limit=1] feet rotated ~ 0 run tp @s ~ ~ ~ ~ 0
execute if score #r rpg_pf matches 5 at @a[distance=..48,gamemode=!spectator,gamemode=!creative,sort=nearest,limit=1] positioned ~-9.5 ~ ~-9.5 positioned over motion_blocking_no_leaves facing entity @a[distance=..16,gamemode=!spectator,gamemode=!creative,sort=nearest,limit=1] feet rotated ~ 0 run tp @s ~ ~ ~ ~ 0
execute if score #r rpg_pf matches 6 at @a[distance=..48,gamemode=!spectator,gamemode=!creative,sort=nearest,limit=1] positioned ~-0.0 ~ ~-13.5 positioned over motion_blocking_no_leaves facing entity @a[distance=..16,gamemode=!spectator,gamemode=!creative,sort=nearest,limit=1] feet rotated ~ 0 run tp @s ~ ~ ~ ~ 0
execute if score #r rpg_pf matches 7 at @a[distance=..48,gamemode=!spectator,gamemode=!creative,sort=nearest,limit=1] positioned ~9.5 ~ ~-9.5 positioned over motion_blocking_no_leaves facing entity @a[distance=..16,gamemode=!spectator,gamemode=!creative,sort=nearest,limit=1] feet rotated ~ 0 run tp @s ~ ~ ~ ~ 0
execute at @s run particle flash{color:16773800} ~ ~1 ~ 0 0 0 0 1 normal
execute at @s run particle end_rod ~ ~1 ~ 0.4 0.8 0.4 0.05 24 normal
execute at @s positioned ~ ~1.3 ~ run function rpg:pope_fight/fx/ring
function rpg:pope_fight/clip/teleport_in
