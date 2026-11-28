bossbar set rpg:prologue_zh_i3 name [{"translate":"rpg.prologue.N03.zh","fallback":"那时神说：将来必有一位子要来，众天使都当向他屈膝。","color":"#BFB8A8","italic":false}]
bossbar set rpg:prologue_en_i3 name [{"translate":"rpg.prologue.N03.en","fallback":"Then God said: A Son shall come, and every angel shall bow the knee to Him.","color":"#BFB8A8","italic":true}]
scoreboard players set #sub rpg_pr_i3 111
scoreboard players set #subn rpg_pr_i3 103
execute as @a[tag=rpg.pri3] at @s run playsound rpg:vo.prologue.n03 voice @s ~ ~ ~ 1 1
