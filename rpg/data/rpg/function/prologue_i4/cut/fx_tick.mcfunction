# 过场里持续的特效：裂缝（#rift 1 张开中 / 2 合上中）、路西法身上的暗红黑气（#aura）、飘向裂缝的绿烟（#smoke）
execute if score #rift rpg_pr_i4 matches 1 in rpg:armageddon_4 run particle minecraft:reverse_portal 0 87.5 -9 2.6 3.6 0.3 0.05 30 force
execute if score #rift rpg_pr_i4 matches 1 in rpg:armageddon_4 run particle minecraft:dust{color:[0.48,0.25,0.75],scale:2.4} 0 87.5 -9 2.4 3.4 0.2 0 10 force
execute if score #rift rpg_pr_i4 matches 1 in rpg:armageddon_4 run particle minecraft:portal 0 87.5 -9 3 4 0.5 0.6 12 force
execute if score #rift rpg_pr_i4 matches 2 in rpg:armageddon_4 run particle minecraft:reverse_portal 0 87.5 -9 1.2 2 0.2 0.02 10 force
# 地下城特效（rpg:michael_vfx）：米迦勒 Boss 不在场时由这里推进
execute unless entity @e[type=minecraft:marker,tag=rpg.mkb.center,limit=1,distance=0..] as @e[tag=rpg.mkb.fx,distance=0..] at @s run function rpg:michael_boss_i4/fx/tick
execute if score #aura rpg_pr_i4 matches 1.. as @e[type=minecraft:vindicator,tag=rpg.pr.a.lucifer,distance=0..] at @s run particle minecraft:dust{color:[0.45,0.05,0.05],scale:1.6} ~ ~1 ~ 0.4 0.8 0.4 0 4 force
execute if score #aura rpg_pr_i4 matches 1.. as @e[type=minecraft:vindicator,tag=rpg.pr.a.lucifer,distance=0..] at @s run particle minecraft:large_smoke ~ ~0.6 ~ 0.3 0.3 0.3 0.01 1 force
execute if score #smoke rpg_pr_i4 matches 1 as @e[type=minecraft:marker,tag=rpg.pr.smoke,distance=0..] at @s run function rpg:prologue_i4/cut/smoke_step
execute unless score #smoke rpg_pr_i4 matches 1 run kill @e[type=minecraft:item_display,tag=rpg.pr.smokev,distance=0..]
# 序列帧（Codex 画的裂缝 rift_0..7、绿烟 smoke_0..7，每 3 刻一帧）
scoreboard players add #fxc rpg_pr_i4 1
execute if score #fxc rpg_pr_i4 matches 3.. run function rpg:prologue_i4/cut/fx_frame
execute if score #rift rpg_pr_i4 matches 1.. unless entity @e[type=minecraft:item_display,tag=rpg.pr.riftv,distance=0..] in rpg:armageddon_4 run summon minecraft:item_display 0 87.5 -9 {Tags:["rpg.pr.riftv","rpg.pr.ent"],billboard:"vertical",brightness:{sky:15,block:15},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:prologue_fx/rift_0"}},item_display:"fixed",transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[14f,17f,14f]}}
execute if score #rift rpg_pr_i4 matches 0 run kill @e[type=minecraft:item_display,tag=rpg.pr.riftv,distance=0..]
