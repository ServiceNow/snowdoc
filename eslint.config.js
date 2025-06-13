/* eslint-config.js */
const jsdoc = require('eslint-plugin-jsdoc');

const SERVICENOW_TYPES = [
  "answer", "current", "previous", "escape", "event", "jelly", "g_request", "g_device", "g_probe", "g_sensor", "session", "gs", "j2js", "parent", "pm", "root", "unescape", "activity", "workflow", "document", "global",
  "AbstractAjaxProcessor", "AbstractScriptProcessor", "AbstractTimelineSchedulePage", "AJAXHelper", "ArrayUtil", "Class", "DurationCalculator", "GenericException", "GlideAbstractExecutionPlan", "GlideAJAXSchedulePage", "GlideAggregate", "GlideAppHome", "GlideAuditor", "GlideARecurrence", "GlideChoiceListGenerator", "GlideController", "GlideDate", "GlideDateTime", "GlideDBMacro", "GlideDBObjectManager", "GlideDBUtil", "GlideDuration", "GlideEvaluator", "GlideFilter", "GlideGroup", "GlideGuid", "GlideHistorySet", "GlideJellyRunner", "GlideLocale", "GlideMobileExtensions", "GlideMultipleDelete", "GlideMultipleUpdate", "GlidePluginManager", "GlideProperties", "GlideQueryString", "GlideRecord", "GlideRecordSecure", "GlideRecordUtil", "GlideSchedule", "GlideScheduleDateTime", "GlideScheduleDateTimeSpan", "GlideScopedEvaluator", "GlideStopWatch", "GlideStringUtil", "GlideSubQuery", "GlideSysAttachment", "GlideSysChoice", "GlideSysLog", "GlideTableDescriptor", "GlideTableHierarchy", "GlideTimelineItem", "GlideTransaction", "GlideURLUtil", "GlideUser", "GlideWikiModel", "GlideXMLDocument", "GlideXMLUtil", "GSLog", "NumberManager", "JSONParser", "JSUtil", "ScheduleValidation", "ScheduleOnce", "SelfCleaningMutex", "SNC", "SOAPMessage", "TableDescriptor", "TableUtils", "UIPolicyBuilder", "Workflow", "WorkflowIconsStages", "XMLDocument", "GlideArchiveTable", "GlideAttachmentIndexDocument", "GlideAttachmentIndexTypes", "GlideAuditDelete", "GlideBootstrap", "GlideCMSPageLink", "GlideCacheManager", "GlideCascadeFromDelete", "GlideChannelManager", "GlideChartFieldColors", "GlideChartGeneratorFactory", "GlideChartUtil", "GlideChartValue", "GlideChoice", "GlideChoiceList", "GlideChoiceListSet", "GlideClientBrowserTimes", "GlideClientNetworkTimes", "GlideClusterMessage", "GlideClusterSynchronizer", "GlideColumnAttributes", "GlideCompiler", "GlideCompositeElement", "GlideContentConfig", "GlideConverter", "GlideCookieMan", "GlideCounter", "GlideCredentials", "GlideCustomerScriptFixer", "GlideDBConfiguration", "GlideDBConfigurationManager", "GlideDBIndex", "GlideDBKeyStoreFactory", "GlideDBPoolTest", "GlideDBPoolTest2", "GlideDBQuery", "GlideDBTypes", "GlideDBUpdate", "GlideDBView", "GlideDataSource", "GlideDateUtil", "GlideDiagram", "GlideDiagramAction", "GlideDiagramEdge", "GlideDiagramNode", "GlideDistUpgradeRunner", "GlideDomainDisplay", "GlideDomainNumberProvider", "GlideDomainPathProvider", "GlideDomainSpoolProvider", "GlideDomainSupport", "GlideDomainTree", "GlideDomainValidator", "GlideElement", "GlideElementDescriptor", "GlideElementPhoneNumber", "GlideElementXMLSerializer", "GlideEmailFormatter", "GlideEmailOutbound", "GlideEmailReader", "GlideEmailSender", "GlideEmailUtil", "GlideEmitter", "GlideEncrypter", "GlideEncryptionUtil", "GlideEventManager", "GlideExcelExporter", "GlideFieldList", "GlideFileUtil", "GlideForm", "GlideGauge", "GlideHTTPClient", "GlideHTTPRequest", "GlideHTTPUtil", "GlideHostUtil", "GlideICALUtil", "GlideIMAPOAuthReader", "GlideIOMonitor", "GlideImportLog", "GlideImportSetLoader", "GlideImportSetTransformer", "GlideIndexDescriptor", "GlideIntegerTime", "GlideInternalElementTypeChoiceList", "GlideInternalMonitor", "GlideInternalSoapClient", "GlideJDBCProbeTestWorker", "GlideJSUtil", "GlideJellyContext", "GlideLDAP", "GlideLDAPConfig", "GlideLDAPConfigurations", "GlideLDAPDiagnostics", "GlideLDAPGroups", "GlideLDAPTestConnectionProcessor", "GlideLDAPTransformQueue", "GlideLDAPUserUpdate", "GlideLRUCache", "GlideLabelUtil", "GlideListLabel", "GlideListM2MBacking", "GlideLog", "GlideMarkupWriter", "GlideMemoryActive", "GlideMemoryCache", "GlideMemorySwap", "GlideMemoryTotal", "GlideMetaData", "GlideMutex", "GlideNumberManager", "GlideObjectManager", "GlideOrderingManager", "GlideOutputWriterFactory", "GlideOverLoadedChoices", "GlidePOP3Reader", "GlidePersonalListDef", "GlidePersonalTaskUtils", "GlidePluginManagerWorker", "GlidePreviewProblemRecord", "GlideProgressMonitor", "GlideProjectTemplate", "GlidePropertiesDB", "GlidePushBackOutWorker", "GlideRecordFactory", "GlideRecordKeySetLoader", "GlideRecordLock", "GlideRecordXMLSerializer", "GlideRelationship", "GlideRelationshipUtil", "GlideRemoteGlideRecord", "GlideRenderProperties", "GlideRequestMap", "GlideRhinoHelper", "GlideRunScriptJob", "GlideSMTPConnection", "GlideSMTPOAuthConnection", "GlideSOAPDocument", "GlideSOAPSigner", "GlideSQLDeleteMonitor", "GlideSQLInsertMonitor", "GlideSQLResponseMonitor", "GlideSQLSelectMonitor", "GlideSQLUpdateMonitor", "GlideScheduleTimeMap", "GlideScheduleTimeSpan", "GlideScopeAPI", "GlideScriptListener", "GlideScriptRecordUtil", "GlideScriptSystemUtilDB", "GlideScriptViewManager", "GlideScriptedHierarchicalWorker", "GlideScriptedProgressWorker", "GlideSecondaryDatabaseConfiguration", "GlideSecurityManager", "GlideSelfCleaningMutex", "GlideServlet", "GlideSession", "GlideSessionDebug", "GlideSimpleHTTPClient", "GlideSimpleScriptListener", "GlideStatus", "GlideStringList", "GlideSummaryTableWriter", "GlideSyncWorker", "GlideSysAttachmentInputStream", "GlideSysBRThreadMonitor", "GlideSysCPUThreadMonitor", "GlideSysConcurrencyMonitor", "GlideSysDBThreadMonitor", "GlideSysDateUtil", "GlideSysField", "GlideSysForm", "GlideSysForms", "GlideSysList", "GlideSysListSaverWorker", "GlideSysMessage", "GlideSysNetThreadMonitor", "GlideSysRelatedList", "GlideSysSection", "GlideSysSectionSaverWorker", "GlideSysThreadMonitor", "GlideSystemDateUtil", "GlideSystemUtil", "GlideSystemUtilDB", "GlideSystemUtilScript", "GlideTableChoiceList", "GlideTableCleaner", "GlideTableCreator", "GlideTemplate", "GlideTextIndexEvent", "GlideThreadAttributes", "GlideThreadUtil", "GlideTime", "GlideTimelineFrameSeparator", "GlideTransactionManager", "GlideTransferAuditDataHelper", "GlideUISession", "GlideURL", "GlideURLUTF8Encoder", "GlideUpdateManager2", "GlideUpdateSet", "GlideUpdateSetPreviewer", "GlideUpdateSetWorker", "GlideUpdateTableChoiceList", "GlideUpgradeArtifactManager", "GlideUpgradeMonitor", "GlideUserGroup", "GlideUtil", "GlideVTBBoardBuilder", "GlideVTBCompatibility", "GlideVersionConflictAction", "GlideWSClient", "GlideWarDeleter", "GlideWarDownloader", "GlideWorkerThreadManager", "GlideXMLParameters", "GlideXMLStats", "GlideappChartParameters", "GlideappECCInputMessage", "GlideappECCOutputMessage", "GlideappECCResponseMessage", "GlideappLiveUtils", "GlideappUpdateVersion", "GlidesoftGlideAttributesImpl", "SncRrdGlideBackendFactory",
  "AssetUtils", "Consumables", "DocumentManagementUtils", "DocumentManagementDB", "GlideappCalculationHelper", "GlideappCart", "GlideappCatalogItem", "GlideappCategory", "GlideappCatItemPopper", "GlideappCategoryPopper", "GlideappDeliveryPlan", "GlideappHome", "GlideappLiveProfile", "GlideappLiveFeedUIAction", "GlideappOrderGuide", "GlideappQuestion", "GlideappRequestItemWorkflow", "GlideappRequestNew", "GlideCatalogCloneWorker", "hr_AbstractSecurityManager", "LiveFeedProfile", "KBCategorySNC", "KBCategory", "KBKnowledge", "KBKnowledgeSNC", "KBKnowledgeBase", "KBKnowledgeBaseSNC", "KBKnowledgeKeyword", "KBKnowledgeKeywordSNC", "KBPropertySNC", "KBRevision", "KBUtilsSNC", "KnowledgeHelp", "SncOnCallRotation", "SMConstants", "TransferOrderLineFilters", "XMLUtil", "last-dummy"
];

module.exports = [
  {
    files: ['**/*.js'],
    languageOptions: {
      ecmaVersion: 2020,
      sourceType: 'script',
      globals: {
        gs: 'readonly',
        j2js: 'readonly',
        TableUtils: 'readonly',
      },
    },
    plugins: { jsdoc },

    settings: {
      jsdoc: {
        tagNamePreference: { constructor: 'constructor' },
      },
    },

    rules: {
      /* ---- keep lightweight hygiene checks ---- */
      'jsdoc/check-alignment': 'error',
      'jsdoc/check-syntax': 'error',
      'jsdoc/check-tag-names': 'warn',

      /* ---- relaxed param/return rules ---- */
      'jsdoc/require-param': 'off',
      'jsdoc/require-param-description': 'off',
      'jsdoc/require-param-type': 'off',
      'jsdoc/require-param-name': 'off',
      'jsdoc/require-returns': 'off',
      'jsdoc/require-returns-description': 'off',
      'jsdoc/require-returns-type': 'off',

      /* ---- type sanity without punishing Glide* ---- */
      'jsdoc/no-undefined-types': ['warn', { definedTypes: SERVICENOW_TYPES }],
      'jsdoc/valid-types': 'warn',

      /* ---- other heavyweight checks disabled ---- */
      'jsdoc/check-param-names': 'off',
      'jsdoc/check-types': 'off',
      'jsdoc/implements-on-classes': 'off',
    },
  },
];
