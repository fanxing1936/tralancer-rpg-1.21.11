bossbar set rpg:prologue_zh_i3 name [{"translate":"rpg.prologue.N04.zh","fallback":"路西法心里说：我要升到天上，我要高举我的宝座，在神众星以上。","color":"#BFB8A8","italic":false}]
bossbar set rpg:prologue_en_i3 name [{"translate":"rpg.prologue.N04.en","fallback":"And Lucifer said in his heart: I will ascend into","color":"#BFB8A8","italic":true}]
scoreboard players set #sub rpg_pr_i3 124
scoreboard players set #subn rpg_pr_i3 104
execute as @a[tag=rpg.pri3] at @s run playsound rpg:vo.prologue.n04 voice @s ~ ~ ~ 1 1
