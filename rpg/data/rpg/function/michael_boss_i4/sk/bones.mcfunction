execute if score @s rpg_mk_t matches 26 run tp @s @e[tag=rpg.mkb.bp1,limit=1,distance=0..]
execute if score @s rpg_mk_t matches 26 run playsound minecraft:item.trident.throw hostile @a[distance=..48] ~ ~ ~ 1.4 0.6
execute if score @s rpg_mk_t matches 34 run execute facing entity @e[tag=rpg.mkb.bp2,limit=1,distance=0..] feet run tp @s ~ ~ ~ ~ 0
execute if score @s rpg_mk_t matches 34 run execute positioned ~ ~0.05 ~ run function rpg:michael_boss_i4/bones/warn
execute if score @s rpg_mk_t matches 40 run function rpg:michael/anim/enter/roll_f
execute if score @s rpg_mk_t matches 40..49 run function rpg:michael_boss_i4/bones/step
execute if score @s rpg_mk_t matches 50 run function rpg:michael/anim/enter/rib_slash4
execute if score @s rpg_mk_t matches 50 run function rpg:michael_boss_i4/bones/hit
execute if score @s rpg_mk_t matches 64 run execute facing entity @e[tag=rpg.mkb.bp1,limit=1,distance=0..] feet run tp @s ~ ~ ~ ~ 0
execute if score @s rpg_mk_t matches 64 run execute positioned ~ ~0.05 ~ run function rpg:michael_boss_i4/bones/warn
execute if score @s rpg_mk_t matches 70 run function rpg:michael/anim/enter/roll_f
execute if score @s rpg_mk_t matches 70..79 run function rpg:michael_boss_i4/bones/step
execute if score @s rpg_mk_t matches 80 run function rpg:michael/anim/enter/rib_slash4
execute if score @s rpg_mk_t matches 80 run function rpg:michael_boss_i4/bones/hit
execute if score @s rpg_mk_t matches 94 run execute facing entity @e[tag=rpg.mkb.bp2,limit=1,distance=0..] feet run tp @s ~ ~ ~ ~ 0
execute if score @s rpg_mk_t matches 94 run execute positioned ~ ~0.05 ~ run function rpg:michael_boss_i4/bones/warn
execute if score @s rpg_mk_t matches 100 run function rpg:michael/anim/enter/roll_f
execute if score @s rpg_mk_t matches 100..109 run function rpg:michael_boss_i4/bones/step
execute if score @s rpg_mk_t matches 110 run function rpg:michael/anim/enter/rib_slash4
execute if score @s rpg_mk_t matches 110 run function rpg:michael_boss_i4/bones/hit
execute if score @s rpg_mk_t matches 124 run execute facing entity @e[tag=rpg.mkb.bp1,limit=1,distance=0..] feet run tp @s ~ ~ ~ ~ 0
execute if score @s rpg_mk_t matches 124 run execute positioned ~ ~0.05 ~ run function rpg:michael_boss_i4/bones/warn
execute if score @s rpg_mk_t matches 130 run function rpg:michael/anim/enter/roll_f
execute if score @s rpg_mk_t matches 130..139 run function rpg:michael_boss_i4/bones/step
execute if score @s rpg_mk_t matches 140 run function rpg:michael/anim/enter/rib_slash4
execute if score @s rpg_mk_t matches 140 run function rpg:michael_boss_i4/bones/hit
execute if score @s rpg_mk_t matches 150 run function rpg:michael_boss_i4/bones/catch
execute if score @s rpg_mk_t matches 160 run function rpg:michael_boss_i4/solid/on
execute if score @s rpg_mk_t matches 160 run scoreboard players set @s rpg_mk_so 40
execute if score @s rpg_mk_t matches 160 run function rpg:michael/anim/enter/idle
execute if score @s rpg_mk_t matches 200.. run function rpg:michael_boss_i4/sk/end
