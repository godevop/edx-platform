// Backbone.js Page Object Factory: Certificates

/**
Notes from Andy Armstrong:
The basic idea of a page factory is that it is a single RequireJS dependency that can be loaded in a template
to create a page object.  This was added for the RequireJS Optimizer, which needs to have a single root to determine
statically all of the dependencies needed by a page.  The RequireJS Optimizer combines these dependencies into a single
optimized JS file. Mako templates typically contain a block that constructs the page object using this page factory.
Unit tests for the page factory verify that it behaves as desired. Some of these factories are more complex than others.
The RequireJS Optimizer is only enabled in Studio at present, so the page factories aren't strictly required in the LMS.
We do intend to enable page factories on the LMS too.
*/

define([
    'js/certificates/collections/certificates',
    'js/certificates/models/certificate',
    'js/certificates/views/certificates_page'
],
function(CertificatesCollection, Certificate, CertificatesPage) {
    'use strict';
    return function (certificatesJson, certificateUrl, courseOutlineUrl) {
        // Initialize the model collection, passing any necessary options to the constructor
        var certificatesCollection = new CertificatesCollection(certificatesJson, {
            parse: true,
            canBeEmpty: true,
            certificateUrl: certificateUrl
        });
        // Execute the page object's rendering workflow
        var certificatesPage = new CertificatesPage({
            el: $('#content'),
            certificatesCollection: certificatesCollection
        }).render();
    };
});
