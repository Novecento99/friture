import QtQuick 2.15
import QtQuick.Window 2.2
import QtQuick.Layouts 1.15
import QtQuick.Shapes 1.15
import Friture 1.0

Item {
    id: yscaleColumn

    SystemPalette { id: systemPalette; colorGroup: SystemPalette.Active }

    required property ScaleDivision scale_division

    readonly property int majorTickLength: 8
    readonly property int minorTickLength: 4

    property int tickLabelMaxWidth: maxTextWidth(scale_division.logicalMajorTicks)

    implicitWidth: colorBar.width + 2 + tickLabelMaxWidth + 3 + majorTickLength

    property double topOverflow: fontMetrics.height / 2

    function maxTextWidth(majorTicks) {
        var maxWidth = 0
        for (var i = 0; i < majorTicks.length; i++) {
            var textWidth = fontMetrics.boundingRect(majorTicks[i].value).width;
            if (textWidth > maxWidth) {
                maxWidth = textWidth;
            }
        }
        return Math.ceil(maxWidth)
    }

    ColorBar {
        id: colorBar
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        width: 2 * majorTickLength
    } 

    FontMetrics {
        id: fontMetrics
    }

    Shape {
        anchors.left: colorBar.right
        anchors.leftMargin: 1

        ShapePath {
            strokeWidth: 1
            strokeColor: systemPalette.windowText
            fillColor: "transparent"

            PathMove { x: 0; y: 0 }
            PathLine { x: 0; y: yscaleColumn.height }
        }
    }

    // QML docs discourage the use of multiple Shape objects. But the Repeater cannot be used inside Shape.
    Repeater {
        model: scale_division.logicalMajorTicks

        Item {
            anchors.left: colorBar.right
            anchors.leftMargin: 1
            
            implicitWidth: majorTickLength

            y: (1. - modelData.logicalValue) * yscaleColumn.height

            Shape {
                ShapePath {
                    strokeWidth: 1
                    strokeColor: systemPalette.windowText
                    fillColor: "transparent"

                    PathMove { x: 0; y: 0 }
                    PathLine { x: majorTickLength; y: 0 }
                }
            }
        }
    }

    Item {
        id: tickLabels
        anchors.left: colorBar.right
        anchors.leftMargin: majorTickLength + 3

        // QML docs discourage the use of multiple Shape objects. But the Repeater cannot be used inside Shape.
        Repeater {
            model: scale_division.logicalMajorTicks

            Item {
                implicitWidth: tickLabelMaxWidth
                y: (1. - modelData.logicalValue) * yscaleColumn.height

                Text {
                    id: tickLabel
                    text: modelData.value
                    anchors.verticalCenter: parent.verticalCenter
                    verticalAlignment: Text.AlignVCenter
                    color: systemPalette.windowText
                }
            }
        }
    }

    // QML docs discourage the use of multiple Shape objects. But the Repeater cannot be used inside Shape.
    Repeater {
        model: scale_division.logicalMinorTicks

        Item {
            y: (1. - modelData.logicalValue) * yscaleColumn.height
            anchors.left: colorBar.right
            anchors.leftMargin: 1
        
            Shape {
                anchors.left: parent.left

                ShapePath {
                    strokeWidth: 1
                    strokeColor: systemPalette.windowText
                    fillColor: "transparent"

                    PathMove { x: 0; y: 0 }
                    PathLine { x: minorTickLength; y: 0 }
                }
            }
        }
    }
}