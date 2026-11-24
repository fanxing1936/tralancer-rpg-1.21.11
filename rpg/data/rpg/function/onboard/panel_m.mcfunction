$data modify storage rpg:onboard tmp.row set from storage rpg:onboard p$(id)
$data modify storage rpg:onboard tmp.row.in set value "$(n)"
$data modify storage rpg:onboard tmp.row.ic set value "$(c)"
function rpg:onboard/panel_line with storage rpg:onboard tmp.row
