# 教廷总动员：先在落点亮起圣印和光柱。
execute store result score #n rpg_pf if entity @e[type=minecraft:vindicator,tag=rpg.pf.unit]
tellraw @a[distance=..48] ["",{"text":"〖教皇〗","color":"#C9A646","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"教廷的军团，听我号令。","color":"#9C9A94","bold":false,"italic":false}]
execute if score #n rpg_pf matches ..3 at @a[distance=..48,gamemode=!spectator,gamemode=!creative,sort=nearest,limit=1] rotated 0 0 positioned ^ ^ ^5 positioned over motion_blocking_no_leaves run function rpg:pope_fight/boss/wave_seal
execute if score #n rpg_pf matches ..2 at @a[distance=..48,gamemode=!spectator,gamemode=!creative,sort=nearest,limit=1] rotated 180 0 positioned ^ ^ ^5 positioned over motion_blocking_no_leaves run function rpg:pope_fight/boss/wave_seal
