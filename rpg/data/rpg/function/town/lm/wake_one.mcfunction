data merge entity @s {NoAI:0b}
tag @s add rpg.lm.awake
execute if entity @s[tag=rpg.lm.inq] run tellraw @a[distance=..32] ["",{"text":"〖审判官〗","color":"#B8902F","bold":true,"italic":false},{"text":"  孤堡的墙不是为挡恶魔造的，是为挡忘了神的人。","color":"#9C9A94","bold":false,"italic":false}]
