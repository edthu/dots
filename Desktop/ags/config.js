import Widget from 'resource:///com/github/Aylur/ags/widget.js';

const myLabel = Widget.Label({
    label: "cool stuff",
})

const labelTwo = Widget.Label({
    label: "amazing",
})

const box = Widget.Box({
	spacing: 8, 
	homogeneous: false,
	vertical: false,
	children:[myLabel, labelTwo],
})

const myBar = Widget.Window({
    name: "bar",
    anchor: ['top', 'left', 'right'],
    child: box,
})

export default {
	windows: [myBar]
}
