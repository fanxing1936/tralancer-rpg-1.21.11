execute at @s facing entity @a[tag=rpg.fo.me,limit=1] feet rotated ~ 0 if block ^ ^ ^-0.5 #rpg:force/pass if block ^ ^1 ^-0.5 #rpg:force/pass run tp @s ^ ^ ^-0.5
execute at @s facing entity @a[tag=rpg.fo.me,limit=1] feet rotated ~ 0 if block ^ ^ ^-0.5 #rpg:force/pass if block ^ ^1 ^-0.5 #rpg:force/pass run tp @s ^ ^ ^-0.5
execute at @s facing entity @a[tag=rpg.fo.me,limit=1] feet rotated ~ 0 if block ^ ^ ^-0.5 #rpg:force/pass if block ^ ^1 ^-0.5 #rpg:force/pass run tp @s ^ ^ ^-0.5
execute at @s facing entity @a[tag=rpg.fo.me,limit=1] feet rotated ~ 0 if block ^ ^ ^-0.5 #rpg:force/pass if block ^ ^1 ^-0.5 #rpg:force/pass run tp @s ^ ^ ^-0.5
execute at @s facing entity @a[tag=rpg.fo.me,limit=1] feet rotated ~ 0 if block ^ ^ ^-0.5 #rpg:force/pass if block ^ ^1 ^-0.5 #rpg:force/pass run tp @s ^ ^ ^-0.5
execute at @s facing entity @a[tag=rpg.fo.me,limit=1] feet rotated ~ 0 if block ^ ^ ^-0.5 #rpg:force/pass if block ^ ^1 ^-0.5 #rpg:force/pass run tp @s ^ ^ ^-0.5
execute if score #lv rpg_fo matches 1 run effect give @s minecraft:weakness 2 1 true
execute if score #lv rpg_fo matches 2 run effect give @s minecraft:weakness 3 1 true
execute if score #lv rpg_fo matches 3 run effect give @s minecraft:weakness 4 1 true
execute if score #lv rpg_fo matches 1 run effect give @s minecraft:slowness 2 1 true
execute if score #lv rpg_fo matches 2 run effect give @s minecraft:slowness 3 1 true
execute if score #lv rpg_fo matches 3 run effect give @s minecraft:slowness 4 1 true
execute at @s run particle minecraft:smoke ~ ~1.8 ~ 0.2 0.2 0.2 0.02 8
