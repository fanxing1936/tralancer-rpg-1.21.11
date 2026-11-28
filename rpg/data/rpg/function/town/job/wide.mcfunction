# 整块町地（±96）：九点群系都得是危险 I–II，5×5 取样高差不过 16
scoreboard players set #ok rpg_tw 1
scoreboard players set #mn rpg_tw 9999
scoreboard players set #mx rpg_tw -9999
$execute in minecraft:overworld positioned $(xm96) 80 $(zm96) unless biome ~ ~ ~ #rpg:town_ok run scoreboard players set #ok rpg_tw 0
$execute in minecraft:overworld positioned $(xm96) 80 $(z) unless biome ~ ~ ~ #rpg:town_ok run scoreboard players set #ok rpg_tw 0
$execute in minecraft:overworld positioned $(xm96) 80 $(zp96) unless biome ~ ~ ~ #rpg:town_ok run scoreboard players set #ok rpg_tw 0
$execute in minecraft:overworld positioned $(x) 80 $(zm96) unless biome ~ ~ ~ #rpg:town_ok run scoreboard players set #ok rpg_tw 0
$execute in minecraft:overworld positioned $(x) 80 $(z) unless biome ~ ~ ~ #rpg:town_ok run scoreboard players set #ok rpg_tw 0
$execute in minecraft:overworld positioned $(x) 80 $(zp96) unless biome ~ ~ ~ #rpg:town_ok run scoreboard players set #ok rpg_tw 0
$execute in minecraft:overworld positioned $(xp96) 80 $(zm96) unless biome ~ ~ ~ #rpg:town_ok run scoreboard players set #ok rpg_tw 0
$execute in minecraft:overworld positioned $(xp96) 80 $(z) unless biome ~ ~ ~ #rpg:town_ok run scoreboard players set #ok rpg_tw 0
$execute in minecraft:overworld positioned $(xp96) 80 $(zp96) unless biome ~ ~ ~ #rpg:town_ok run scoreboard players set #ok rpg_tw 0
$execute in minecraft:overworld positioned $(xm96) 0 $(zm96) positioned over motion_blocking_no_leaves run function rpg:town/s/mm
$execute in minecraft:overworld positioned $(xm96) 0 $(zm48) positioned over motion_blocking_no_leaves run function rpg:town/s/mm
$execute in minecraft:overworld positioned $(xm96) 0 $(z) positioned over motion_blocking_no_leaves run function rpg:town/s/mm
$execute in minecraft:overworld positioned $(xm96) 0 $(zp48) positioned over motion_blocking_no_leaves run function rpg:town/s/mm
$execute in minecraft:overworld positioned $(xm96) 0 $(zp96) positioned over motion_blocking_no_leaves run function rpg:town/s/mm
$execute in minecraft:overworld positioned $(xm48) 0 $(zm96) positioned over motion_blocking_no_leaves run function rpg:town/s/mm
$execute in minecraft:overworld positioned $(xm48) 0 $(zm48) positioned over motion_blocking_no_leaves run function rpg:town/s/mm
$execute in minecraft:overworld positioned $(xm48) 0 $(z) positioned over motion_blocking_no_leaves run function rpg:town/s/mm
$execute in minecraft:overworld positioned $(xm48) 0 $(zp48) positioned over motion_blocking_no_leaves run function rpg:town/s/mm
$execute in minecraft:overworld positioned $(xm48) 0 $(zp96) positioned over motion_blocking_no_leaves run function rpg:town/s/mm
$execute in minecraft:overworld positioned $(x) 0 $(zm96) positioned over motion_blocking_no_leaves run function rpg:town/s/mm
$execute in minecraft:overworld positioned $(x) 0 $(zm48) positioned over motion_blocking_no_leaves run function rpg:town/s/mm
$execute in minecraft:overworld positioned $(x) 0 $(z) positioned over motion_blocking_no_leaves run function rpg:town/s/mm
$execute in minecraft:overworld positioned $(x) 0 $(zp48) positioned over motion_blocking_no_leaves run function rpg:town/s/mm
$execute in minecraft:overworld positioned $(x) 0 $(zp96) positioned over motion_blocking_no_leaves run function rpg:town/s/mm
$execute in minecraft:overworld positioned $(xp48) 0 $(zm96) positioned over motion_blocking_no_leaves run function rpg:town/s/mm
$execute in minecraft:overworld positioned $(xp48) 0 $(zm48) positioned over motion_blocking_no_leaves run function rpg:town/s/mm
$execute in minecraft:overworld positioned $(xp48) 0 $(z) positioned over motion_blocking_no_leaves run function rpg:town/s/mm
$execute in minecraft:overworld positioned $(xp48) 0 $(zp48) positioned over motion_blocking_no_leaves run function rpg:town/s/mm
$execute in minecraft:overworld positioned $(xp48) 0 $(zp96) positioned over motion_blocking_no_leaves run function rpg:town/s/mm
$execute in minecraft:overworld positioned $(xp96) 0 $(zm96) positioned over motion_blocking_no_leaves run function rpg:town/s/mm
$execute in minecraft:overworld positioned $(xp96) 0 $(zm48) positioned over motion_blocking_no_leaves run function rpg:town/s/mm
$execute in minecraft:overworld positioned $(xp96) 0 $(z) positioned over motion_blocking_no_leaves run function rpg:town/s/mm
$execute in minecraft:overworld positioned $(xp96) 0 $(zp48) positioned over motion_blocking_no_leaves run function rpg:town/s/mm
$execute in minecraft:overworld positioned $(xp96) 0 $(zp96) positioned over motion_blocking_no_leaves run function rpg:town/s/mm
scoreboard players operation #sp rpg_tw = #mx rpg_tw
scoreboard players operation #sp rpg_tw -= #mn rpg_tw
execute if score #sp rpg_tw matches 17.. run scoreboard players set #ok rpg_tw 0
execute if score #mn rpg_tw matches ..62 run scoreboard players set #ok rpg_tw 0
execute if score #ok rpg_tw matches 1 run scoreboard players operation #h0 rpg_tw = #mn rpg_tw
execute if score #ok rpg_tw matches 1 run scoreboard players operation #h0 rpg_tw += #mx rpg_tw
execute if score #ok rpg_tw matches 1 run scoreboard players operation #h0 rpg_tw /= #2 rpg_tw
