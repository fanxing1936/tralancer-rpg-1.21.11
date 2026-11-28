# 告示板「现在就开始」（as 玩家，#t = 镇号）
execute if score #run rpg_te matches 1.. run return run tellraw @s ["",{"text":"〖副本〗","color":"#C9A646","bold":true,"italic":false},{"text":"  别处的副本还没打完，稍等。","color":"#9C9A94","bold":false,"italic":false}]
execute if score #t rpg_tl matches 1 if score #es1 rpg_te matches 1.. run return run tellraw @s ["",{"text":"〖副本〗","color":"#C9A646","bold":true,"italic":false},{"text":"  今天的已经打过了。","color":"#9C9A94","bold":false,"italic":false}]
execute if score #t rpg_tl matches 1 if score #ev1 rpg_te matches 0 run execute store result score #ev1 rpg_te run random value 1..3
execute if score #t rpg_tl matches 1 run return run function rpg:town/ev/begin {t:1}
execute if score #t rpg_tl matches 2 if score #es2 rpg_te matches 1.. run return run tellraw @s ["",{"text":"〖副本〗","color":"#C9A646","bold":true,"italic":false},{"text":"  今天的已经打过了。","color":"#9C9A94","bold":false,"italic":false}]
execute if score #t rpg_tl matches 2 if score #ev2 rpg_te matches 0 run execute store result score #ev2 rpg_te run random value 1..3
execute if score #t rpg_tl matches 2 run return run function rpg:town/ev/begin {t:2}
execute if score #t rpg_tl matches 3 if score #es3 rpg_te matches 1.. run return run tellraw @s ["",{"text":"〖副本〗","color":"#C9A646","bold":true,"italic":false},{"text":"  今天的已经打过了。","color":"#9C9A94","bold":false,"italic":false}]
execute if score #t rpg_tl matches 3 if score #ev3 rpg_te matches 0 run execute store result score #ev3 rpg_te run random value 1..3
execute if score #t rpg_tl matches 3 run return run function rpg:town/ev/begin {t:3}
execute if score #t rpg_tl matches 4 if score #es4 rpg_te matches 1.. run return run tellraw @s ["",{"text":"〖副本〗","color":"#C9A646","bold":true,"italic":false},{"text":"  今天的已经打过了。","color":"#9C9A94","bold":false,"italic":false}]
execute if score #t rpg_tl matches 4 if score #ev4 rpg_te matches 0 run execute store result score #ev4 rpg_te run random value 1..3
execute if score #t rpg_tl matches 4 run return run function rpg:town/ev/begin {t:4}
execute if score #t rpg_tl matches 5 if score #es5 rpg_te matches 1.. run return run tellraw @s ["",{"text":"〖副本〗","color":"#C9A646","bold":true,"italic":false},{"text":"  今天的已经打过了。","color":"#9C9A94","bold":false,"italic":false}]
execute if score #t rpg_tl matches 5 if score #ev5 rpg_te matches 0 run execute store result score #ev5 rpg_te run random value 1..3
execute if score #t rpg_tl matches 5 run return run function rpg:town/ev/begin {t:5}
execute if score #t rpg_tl matches 6 if score #es6 rpg_te matches 1.. run return run tellraw @s ["",{"text":"〖副本〗","color":"#C9A646","bold":true,"italic":false},{"text":"  今天的已经打过了。","color":"#9C9A94","bold":false,"italic":false}]
execute if score #t rpg_tl matches 6 if score #ev6 rpg_te matches 0 run execute store result score #ev6 rpg_te run random value 1..3
execute if score #t rpg_tl matches 6 run return run function rpg:town/ev/begin {t:6}
execute if score #t rpg_tl matches 7 if score #es7 rpg_te matches 1.. run return run tellraw @s ["",{"text":"〖副本〗","color":"#C9A646","bold":true,"italic":false},{"text":"  今天的已经打过了。","color":"#9C9A94","bold":false,"italic":false}]
execute if score #t rpg_tl matches 7 if score #ev7 rpg_te matches 0 run execute store result score #ev7 rpg_te run random value 1..3
execute if score #t rpg_tl matches 7 run return run function rpg:town/ev/begin {t:7}
execute if score #t rpg_tl matches 8 if score #es8 rpg_te matches 1.. run return run tellraw @s ["",{"text":"〖副本〗","color":"#C9A646","bold":true,"italic":false},{"text":"  今天的已经打过了。","color":"#9C9A94","bold":false,"italic":false}]
execute if score #t rpg_tl matches 8 if score #ev8 rpg_te matches 0 run execute store result score #ev8 rpg_te run random value 1..3
execute if score #t rpg_tl matches 8 run return run function rpg:town/ev/begin {t:8}
execute if score #t rpg_tl matches 9 if score #es9 rpg_te matches 1.. run return run tellraw @s ["",{"text":"〖副本〗","color":"#C9A646","bold":true,"italic":false},{"text":"  今天的已经打过了。","color":"#9C9A94","bold":false,"italic":false}]
execute if score #t rpg_tl matches 9 if score #ev9 rpg_te matches 0 run execute store result score #ev9 rpg_te run random value 1..3
execute if score #t rpg_tl matches 9 run return run function rpg:town/ev/begin {t:9}
execute if score #t rpg_tl matches 10 if score #es10 rpg_te matches 1.. run return run tellraw @s ["",{"text":"〖副本〗","color":"#C9A646","bold":true,"italic":false},{"text":"  今天的已经打过了。","color":"#9C9A94","bold":false,"italic":false}]
execute if score #t rpg_tl matches 10 if score #ev10 rpg_te matches 0 run execute store result score #ev10 rpg_te run random value 1..3
execute if score #t rpg_tl matches 10 run return run function rpg:town/ev/begin {t:10}
execute if score #t rpg_tl matches 11 if score #es11 rpg_te matches 1.. run return run tellraw @s ["",{"text":"〖副本〗","color":"#C9A646","bold":true,"italic":false},{"text":"  今天的已经打过了。","color":"#9C9A94","bold":false,"italic":false}]
execute if score #t rpg_tl matches 11 if score #ev11 rpg_te matches 0 run execute store result score #ev11 rpg_te run random value 1..3
execute if score #t rpg_tl matches 11 run return run function rpg:town/ev/begin {t:11}
execute if score #t rpg_tl matches 12 if score #es12 rpg_te matches 1.. run return run tellraw @s ["",{"text":"〖副本〗","color":"#C9A646","bold":true,"italic":false},{"text":"  今天的已经打过了。","color":"#9C9A94","bold":false,"italic":false}]
execute if score #t rpg_tl matches 12 if score #ev12 rpg_te matches 0 run execute store result score #ev12 rpg_te run random value 1..3
execute if score #t rpg_tl matches 12 run return run function rpg:town/ev/begin {t:12}
execute if score #t rpg_tl matches 13 if score #es13 rpg_te matches 1.. run return run tellraw @s ["",{"text":"〖副本〗","color":"#C9A646","bold":true,"italic":false},{"text":"  今天的已经打过了。","color":"#9C9A94","bold":false,"italic":false}]
execute if score #t rpg_tl matches 13 if score #ev13 rpg_te matches 0 run execute store result score #ev13 rpg_te run random value 1..3
execute if score #t rpg_tl matches 13 run return run function rpg:town/ev/begin {t:13}
execute if score #t rpg_tl matches 14 if score #es14 rpg_te matches 1.. run return run tellraw @s ["",{"text":"〖副本〗","color":"#C9A646","bold":true,"italic":false},{"text":"  今天的已经打过了。","color":"#9C9A94","bold":false,"italic":false}]
execute if score #t rpg_tl matches 14 if score #ev14 rpg_te matches 0 run execute store result score #ev14 rpg_te run random value 1..3
execute if score #t rpg_tl matches 14 run return run function rpg:town/ev/begin {t:14}
execute if score #t rpg_tl matches 15 if score #es15 rpg_te matches 1.. run return run tellraw @s ["",{"text":"〖副本〗","color":"#C9A646","bold":true,"italic":false},{"text":"  今天的已经打过了。","color":"#9C9A94","bold":false,"italic":false}]
execute if score #t rpg_tl matches 15 if score #ev15 rpg_te matches 0 run execute store result score #ev15 rpg_te run random value 1..3
execute if score #t rpg_tl matches 15 run return run function rpg:town/ev/begin {t:15}
execute if score #t rpg_tl matches 16 if score #es16 rpg_te matches 1.. run return run tellraw @s ["",{"text":"〖副本〗","color":"#C9A646","bold":true,"italic":false},{"text":"  今天的已经打过了。","color":"#9C9A94","bold":false,"italic":false}]
execute if score #t rpg_tl matches 16 if score #ev16 rpg_te matches 0 run execute store result score #ev16 rpg_te run random value 1..3
execute if score #t rpg_tl matches 16 run return run function rpg:town/ev/begin {t:16}
execute if score #t rpg_tl matches 17 if score #es17 rpg_te matches 1.. run return run tellraw @s ["",{"text":"〖副本〗","color":"#C9A646","bold":true,"italic":false},{"text":"  今天的已经打过了。","color":"#9C9A94","bold":false,"italic":false}]
execute if score #t rpg_tl matches 17 if score #ev17 rpg_te matches 0 run execute store result score #ev17 rpg_te run random value 1..3
execute if score #t rpg_tl matches 17 run return run function rpg:town/ev/begin {t:17}
execute if score #t rpg_tl matches 18 if score #es18 rpg_te matches 1.. run return run tellraw @s ["",{"text":"〖副本〗","color":"#C9A646","bold":true,"italic":false},{"text":"  今天的已经打过了。","color":"#9C9A94","bold":false,"italic":false}]
execute if score #t rpg_tl matches 18 if score #ev18 rpg_te matches 0 run execute store result score #ev18 rpg_te run random value 1..3
execute if score #t rpg_tl matches 18 run return run function rpg:town/ev/begin {t:18}
execute if score #t rpg_tl matches 19 if score #es19 rpg_te matches 1.. run return run tellraw @s ["",{"text":"〖副本〗","color":"#C9A646","bold":true,"italic":false},{"text":"  今天的已经打过了。","color":"#9C9A94","bold":false,"italic":false}]
execute if score #t rpg_tl matches 19 if score #ev19 rpg_te matches 0 run execute store result score #ev19 rpg_te run random value 1..3
execute if score #t rpg_tl matches 19 run return run function rpg:town/ev/begin {t:19}
execute if score #t rpg_tl matches 20 if score #es20 rpg_te matches 1.. run return run tellraw @s ["",{"text":"〖副本〗","color":"#C9A646","bold":true,"italic":false},{"text":"  今天的已经打过了。","color":"#9C9A94","bold":false,"italic":false}]
execute if score #t rpg_tl matches 20 if score #ev20 rpg_te matches 0 run execute store result score #ev20 rpg_te run random value 1..3
execute if score #t rpg_tl matches 20 run return run function rpg:town/ev/begin {t:20}
