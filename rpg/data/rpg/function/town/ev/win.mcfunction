# 成功：全额奖励
tellraw @a[tag=rpg.tw.in] ["",{"text":"〖副本〗","color":"#C9A646","bold":true,"italic":false},{"text":"  副本完成。","color":"#9C9A94","bold":false,"italic":false}]
execute as @a[tag=rpg.tw.in] run function rpg:town/ev/reward_full
function rpg:town/ev/stop
