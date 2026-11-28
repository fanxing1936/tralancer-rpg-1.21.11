# 判断候选点（用户 2026-11-28：小镇只建在完全平坦的地方）：九点都是危险 I–II 的群系，5×5 取样高差不过 8，不在水上；之后整块削平
scoreboard players set #ok rpg_tw 1
scoreboard players set #mn rpg_tw 9999
scoreboard players set #mx rpg_tw -9999
$execute in minecraft:overworld positioned $(xm40) 80 $(zm40) run function rpg:town/s/bio
$execute in minecraft:overworld positioned $(xm40) 80 $(z) run function rpg:town/s/bio
$execute in minecraft:overworld positioned $(xm40) 80 $(zp40) run function rpg:town/s/bio
$execute in minecraft:overworld positioned $(x) 80 $(zm40) run function rpg:town/s/bio
$execute in minecraft:overworld positioned $(x) 80 $(z) run function rpg:town/s/bio
$execute in minecraft:overworld positioned $(x) 80 $(zp40) run function rpg:town/s/bio
$execute in minecraft:overworld positioned $(xp40) 80 $(zm40) run function rpg:town/s/bio
$execute in minecraft:overworld positioned $(xp40) 80 $(z) run function rpg:town/s/bio
$execute in minecraft:overworld positioned $(xp40) 80 $(zp40) run function rpg:town/s/bio
execute if score #ok rpg_tw matches 0 run return 0
$execute in minecraft:overworld positioned $(xm40) 0 $(zm40) positioned over motion_blocking_no_leaves run function rpg:town/s/mm
$execute in minecraft:overworld positioned $(xm40) 0 $(zm20) positioned over motion_blocking_no_leaves run function rpg:town/s/mm
$execute in minecraft:overworld positioned $(xm40) 0 $(z) positioned over motion_blocking_no_leaves run function rpg:town/s/mm
$execute in minecraft:overworld positioned $(xm40) 0 $(zp20) positioned over motion_blocking_no_leaves run function rpg:town/s/mm
$execute in minecraft:overworld positioned $(xm40) 0 $(zp40) positioned over motion_blocking_no_leaves run function rpg:town/s/mm
$execute in minecraft:overworld positioned $(xm20) 0 $(zm40) positioned over motion_blocking_no_leaves run function rpg:town/s/mm
$execute in minecraft:overworld positioned $(xm20) 0 $(zm20) positioned over motion_blocking_no_leaves run function rpg:town/s/mm
$execute in minecraft:overworld positioned $(xm20) 0 $(z) positioned over motion_blocking_no_leaves run function rpg:town/s/mm
$execute in minecraft:overworld positioned $(xm20) 0 $(zp20) positioned over motion_blocking_no_leaves run function rpg:town/s/mm
$execute in minecraft:overworld positioned $(xm20) 0 $(zp40) positioned over motion_blocking_no_leaves run function rpg:town/s/mm
$execute in minecraft:overworld positioned $(x) 0 $(zm40) positioned over motion_blocking_no_leaves run function rpg:town/s/mm
$execute in minecraft:overworld positioned $(x) 0 $(zm20) positioned over motion_blocking_no_leaves run function rpg:town/s/mm
$execute in minecraft:overworld positioned $(x) 0 $(z) positioned over motion_blocking_no_leaves run function rpg:town/s/mm
$execute in minecraft:overworld positioned $(x) 0 $(zp20) positioned over motion_blocking_no_leaves run function rpg:town/s/mm
$execute in minecraft:overworld positioned $(x) 0 $(zp40) positioned over motion_blocking_no_leaves run function rpg:town/s/mm
$execute in minecraft:overworld positioned $(xp20) 0 $(zm40) positioned over motion_blocking_no_leaves run function rpg:town/s/mm
$execute in minecraft:overworld positioned $(xp20) 0 $(zm20) positioned over motion_blocking_no_leaves run function rpg:town/s/mm
$execute in minecraft:overworld positioned $(xp20) 0 $(z) positioned over motion_blocking_no_leaves run function rpg:town/s/mm
$execute in minecraft:overworld positioned $(xp20) 0 $(zp20) positioned over motion_blocking_no_leaves run function rpg:town/s/mm
$execute in minecraft:overworld positioned $(xp20) 0 $(zp40) positioned over motion_blocking_no_leaves run function rpg:town/s/mm
$execute in minecraft:overworld positioned $(xp40) 0 $(zm40) positioned over motion_blocking_no_leaves run function rpg:town/s/mm
$execute in minecraft:overworld positioned $(xp40) 0 $(zm20) positioned over motion_blocking_no_leaves run function rpg:town/s/mm
$execute in minecraft:overworld positioned $(xp40) 0 $(z) positioned over motion_blocking_no_leaves run function rpg:town/s/mm
$execute in minecraft:overworld positioned $(xp40) 0 $(zp20) positioned over motion_blocking_no_leaves run function rpg:town/s/mm
$execute in minecraft:overworld positioned $(xp40) 0 $(zp40) positioned over motion_blocking_no_leaves run function rpg:town/s/mm
scoreboard players operation #sp rpg_tw = #mx rpg_tw
scoreboard players operation #sp rpg_tw -= #mn rpg_tw
execute if score #sp rpg_tw matches 9.. run scoreboard players set #ok rpg_tw 0
execute if score #mn rpg_tw matches ..62 run scoreboard players set #ok rpg_tw 0
scoreboard players set #v rpg_tw 0
$execute in minecraft:overworld positioned $(x) 80 $(z) if biome ~ ~ ~ #rpg:town_snow run scoreboard players set #v rpg_tw 1
$execute in minecraft:overworld positioned $(x) 80 $(z) if biome ~ ~ ~ #rpg:town_desert run scoreboard players set #v rpg_tw 2
