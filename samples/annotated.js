/**
 * Checks if a child table extends a parent table
 * 
 * @param {string} parent - The name of the parent table
 * @param {string} child - The name of the potential child table
 * @returns {boolean} True if child extends parent, false otherwise
 */
function isTableExtended(parent, child){
    gs.include("j2js");
    /**
     * @class TableExtensionUtil
     * @classdesc Utility for checking table extension relationships.
     *
     * This utility provides methods to determine if a specific table extends another table
     * within the ServiceNow platform. It leverages the TableUtils API to identify parent-child
     * table relationships and extension hierarchies.
     *
     * @author Auto-Generated
     * @version 1.0.0
     */
    var tu = new TableUtils(parent);
    if(tu.tableExists() && tu.hasExtensions()){
        var tableArrayList = tu.getTableExtensions();
        var tableArray = j2js(tableArrayList);
        if(tableArray.indexOf(child) > -1){
            return true;
        }else{
            return false;
        }
    }else{
        return false;
    }
}

// TODO: Could not automatically inject the following doc block:
/**
 * @constructor
 * @description Initialise the TableExtensionUtil class
 */