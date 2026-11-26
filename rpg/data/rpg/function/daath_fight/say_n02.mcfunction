scoreboard players operation #n rpg_dt = @a[tag=rpg.dt.me,limit=1] rpg_dt_n
scoreboard players add #n rpg_dt 1
tellraw @a[tag=rpg.dt.me,limit=1] ["",{"text":"〖","color":"#7C8593","bold":true,"italic":false},{"text":"影","color":"#AAB4C3","bold":true,"italic":false},{"text":"〗","color":"#7C8593","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"这是第 ","color":"#E6DFCF","bold":false,"italic":false},{"score":{"name":"#n","objective":"rpg_dt"},"color":"#FFFFFF","bold":true},{"text":" 次。","color":"#E6DFCF","bold":false,"italic":false}]
